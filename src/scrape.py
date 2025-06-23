import time, arxiv
from query_builder import build_query
from db import get_conn
from config import MAX_RESULTS
from keybert import KeyBERT
import os
import pathlib

os.environ["HF_HOME"]                    = "/data"
os.environ["HF_HUB_CACHE"]               = "/data"
os.environ["TRANSFORMERS_CACHE"]         = "/data"
os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/data"


_kw = KeyBERT(
    "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"cache_folder": "/data"}   # <- same writable path
)

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

