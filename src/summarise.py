from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from db import get_conn
from config import MODEL_NAME

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
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        #load_in_4bit=True, 
        device_map="auto"
    )
    tok   = AutoTokenizer.from_pretrained(MODEL_NAME)
    tok.pad_token = tok.eos_token
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tok,
        do_sample=False,
        return_full_text=False,
    )

# ---------------------------------------------------------------------- #
def summarise_pending():
    pipe = load_pipe()
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, abstract FROM papers WHERE summary IS NULL"
    ).fetchall()

    for pid, abstract in rows:
        out = pipe(PROMPT.format(abstract=abstract), max_new_tokens=150)[0]["generated_text"]
        conn.execute("UPDATE papers SET summary=? WHERE id=?", (out.strip(), pid))

    conn.commit()
    return len(rows)

