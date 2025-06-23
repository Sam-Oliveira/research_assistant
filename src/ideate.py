import textwrap
from summarise import load_pipe
from scrape     import scrape
from db         import get_conn
from typing import Optional,List
from helpers   import rows_by_tag

IDEA_PROMPT = (
   " You are a senior ML researcher. CONTEXT provides a list of papers. From this list of papers, propose THREE new research projects."
    "For each research project proposed, give a new Title, one-sentence on Motivation and background, two-sentences on the new method, "
    "and one-sentence on Evaluation method.\n"
    "===CONTEXT===\n"
    "{context}\n"
    "===PROJECT IDEAS===\n"
)

# ---------------------------------------------------------------------- #
def ideate_from_topic(topic: str, k: int = 8) -> Optional[str]:
    rows = rows_by_tag(topic, k)
    if not rows:
        return None

    ctx  = "\n".join(f"- {t}: {s}" for t, _, s, _ in rows)
    llm  = load_pipe()
    return llm(IDEA_PROMPT.format(context=ctx),
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

    if not ctx:
        return None

    llm = load_pipe()
    return llm(IDEA_PROMPT.format(context="\n".join(ctx)),
               do_sample=False)[0]['generated_text'].strip()