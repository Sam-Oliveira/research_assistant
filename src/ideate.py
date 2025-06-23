import textwrap
from summarise import load_pipe
from scrape     import scrape
from db         import get_conn
from typing import Optional,List
from helpers   import rows_by_tag

IDEA_PROMPT = textwrap.dedent("""\
    You are a senior ML researcher. Using the CONTEXT, propose THREE fresh research projects.
    For each give a new **Title**, one-sentence **Motivation**, two-sentence **Method idea**, and one-sentence **Evaluation method**.

    ===CONTEXT===
    {context}
    ===PROJECT IDEAS===
""")

# ---------------------------------------------------------------------- #
def ideate_from_topic(topic: str, k: int = 8) -> Optional[str]:
    rows = rows_by_tag(topic, k)
    if not rows:                   # <- nothing in DB
        return None

    ctx  = "\n".join(f"- {t}: {s}" for t, _, s, _ in rows)
    llm  = load_pipe()
    return llm(IDEA_PROMPT.format(ctx=ctx), max_new_tokens=300,
               do_sample=False)[0]['generated_text'].strip()

# ------------------------------------------------------------------ #
def ideate_from_ids(ids: List[str]) -> Optional[str]:
    from db import get_conn
    conn = get_conn()
    ctx = []
    for pid in ids:
        row = conn.execute(
            "SELECT title, summary FROM papers WHERE id=?", (pid,)
        ).fetchone()
        if row:
            ctx.append(f"- {row[0]}: {row[1]}")

    if not ctx:                          # <- none of the IDs are in DB
        return None

    llm = load_pipe()
    return llm(IDEA_PROMPT.format(ctx="\n".join(ctx)), max_new_tokens=300,
               do_sample=False)[0]['generated_text'].strip()