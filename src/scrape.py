import time, arxiv
from query_builder import build_query
from db import get_conn
from config import MAX_RESULTS
import os
import pathlib
import os, pathlib, uuid, shutil

BASE_CACHE = pathlib.Path("/data")              # always writable in Spaces
CACHE_DIR  = BASE_CACHE / "hf_cache" / str(os.getpid())

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 1) Point every HF-related lib there
os.environ["HF_HOME"]                    = str(CACHE_DIR)
os.environ["HF_HUB_CACHE"]               = str(CACHE_DIR)
os.environ["TRANSFORMERS_CACHE"]         = str(CACHE_DIR)
os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(CACHE_DIR)

# 2) Remove any stale lock that might have been copied along
lock_file = CACHE_DIR / ".lock"
if lock_file.exists():
    lock_file.unlink()

# 3) Now import and load the model safely
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

st_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder=str(CACHE_DIR)
)
kw_model = KeyBERT(st_model)

def make_tags(title, abstract, top_n=5):
    """
    Extract keywords from the title and abstract using KeyBERT.
    """
    phrases = _kw.extract_keywords(f"{title}. {abstract}",
                                   top_n=top_n,
                                   stop_words="english",
                                   use_mmr=True)
    return ", ".join(p for p, _ in phrases)

def scrape(max_results=MAX_RESULTS, **criteria):
    query  = build_query(**criteria)
    search = arxiv.Search(query=query,
                          max_results=max_results,
                          sort_by=arxiv.SortCriterion.SubmittedDate)

    conn = get_conn()
    for p in search.results():
        tags = make_tags(p.title, p.summary)
        conn.execute(
            "INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?,?)",
            (
                p.entry_id,
                p.title,
                ", ".join(a.name for a in p.authors),
                p.summary,
                p.published.isoformat(),
                None,          # summary placeholder
                tags
            ),
        )
        time.sleep(1)
    conn.commit()

