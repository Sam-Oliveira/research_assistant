import time, arxiv
from query_builder import build_query
from db import get_conn
from config import MAX_RESULTS
import os, pathlib, tempfile,uuid, shutil

# set-up code for huggingface spaces
CACHE_DIR = pathlib.Path(tempfile.gettempdir()) / "hf_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)      # guaranteed writable

for var in (
    "HF_HOME",
    "HF_HUB_CACHE",
    "TRANSFORMERS_CACHE",
    "SENTENCE_TRANSFORMERS_HOME",
):
    os.environ[var] = str(CACHE_DIR)

os.environ["XDG_CACHE_HOME"] = str(pathlib.Path(tempfile.gettempdir()) / ".cache")

from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

st_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder=str(CACHE_DIR)          # explicit path
)
kw_model = KeyBERT(st_model)

"""
# For my Mac
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
# Use a writable cache directory on macOS
cache_dir = os.path.expanduser("~/cache")
os.makedirs(cache_dir, exist_ok=True)

os.environ["HF_HOME"]                    = cache_dir
os.environ["HF_HUB_CACHE"]               = cache_dir
os.environ["TRANSFORMERS_CACHE"]         = cache_dir
os.environ["SENTENCE_TRANSFORMERS_HOME"] = cache_dir


st_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder=cache_dir                 # <- writable
)
kw_model = KeyBERT(st_model)
"""

def make_tags(title, abstract, top_n=5):
    """
    Extract keywords from the title and abstract using KeyBERT.
    """
    phrases = kw_model.extract_keywords(f"{title}. {abstract}",
                                   top_n=top_n,
                                   stop_words="english",
                                   use_mmr=True)
    return ", ".join(p for p, _ in phrases)

def scrape(max_results=MAX_RESULTS, **criteria):
    query  = build_query(**criteria)
    search = arxiv.Search(query=query,
                          max_results=max_results * 3,  # Get more results to filter from
                          sort_by=arxiv.SortCriterion.SubmittedDate)

    conn = get_conn()
    search_results = []  # Track papers from current search that aren't in database
    papers_added = 0
    
    for p in search.results():
        # Check if paper already exists in database
        existing = conn.execute("SELECT id FROM papers WHERE id=?", (p.entry_id,)).fetchone()
        
        if not existing and papers_added < max_results:
            # Paper doesn't exist, add it
            tags = make_tags(p.title, p.summary)
            conn.execute(
                "INSERT INTO papers VALUES (?,?,?,?,?,?,?)",
                (
                    p.entry_id,
                    p.title,
                    ", ".join(a.name for a in p.authors),
                    p.summary,
                    p.published.isoformat(),
                    None,          #  ummary placeholder
                    tags
                ),
            )
            
            # Add to search results
            search_results.append({
                'title': p.title,
                'authors': ", ".join(a.name for a in p.authors),
                'abstract': p.summary,
                'published': p.published.isoformat()
            })
            papers_added += 1
        
        # Stop if enough papers have been added
        if papers_added >= max_results:
            break
            
        time.sleep(1)
    
    conn.commit()
    return search_results

