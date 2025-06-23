from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from db import get_conn
from config import MODEL_NAME
from helpers    import rows_by_tag 
import os
import tempfile
import pathlib
""" 
Summarise the abstract of a paper using a LLM. Further versions should instead summarise the full paper.
"""

PROMPT = (
    "You are a research assistant. Summarise the abstract below in 5 or less bullet points, "
    "highlighting method and key findings.\n"
    "===ABSTRACT===\n{abstract}\n"
    "===SUMMARY===\n"
)

# ---------------------------------------------------------------------- #
def load_pipe():
    cache_dir = pathlib.Path(tempfile.gettempdir()) / "hf_cache"
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        cache_dir=cache_dir,
        device_map="auto"
    )
    tok   = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=cache_dir)
    tok.pad_token = tok.eos_token
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tok,
        do_sample=False,
        return_full_text=False,
    )


def summarise_by_tag(keyword: str, limit: int = 10) -> int:
    """
    Generate summaries only for rows whose tags match `keyword`
    AND whose summary is still NULL.
    Returns number of rows updated.
    """
    pipe = load_pipe()
    conn = get_conn()

    # 1) get IDs + abstracts for matching rows with summary IS NULL
    like = f"%{keyword.lower()}%"
    rows = conn.execute(
        "SELECT id, abstract FROM papers "
        "WHERE summary IS NULL AND LOWER(tags) LIKE ? "
        "ORDER BY published DESC LIMIT ?", (like, limit)
    ).fetchall()

    # 2) run the LLM only on those
    for id, abstract in rows:
        out = pipe(PROMPT.format(abstract=abstract), max_new_tokens=150)[0]['generated_text']
        conn.execute("UPDATE papers SET summary=? WHERE id=?", (out.strip(), id))

    conn.commit()
    return len(rows)

