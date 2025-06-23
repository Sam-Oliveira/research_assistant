import html, sqlite3
from db import get_conn

def render_rows(rows):
    """
    Render rows as HTML.

    Example:
    render_rows(rows_by_tag("diffusion models"))
    """
    blocks = []
    for t, a, txt, pub in rows:
        blocks += [
            f"<h3>{html.escape(t)}</h3>",
            f"<p><b>Authors:</b> {html.escape(a)} <br><i>{pub[:10]}</i></p>",
            f"<pre style='white-space:pre-wrap'>{html.escape(txt)}</pre>",
            "<hr>"
        ]
    return "\n".join(blocks) or "<p>No matching papers found.</p>"

def rows_by_tag(keyword: str, limit: int = 25):
    """
    Get rows in databaseby tag.

    Example:
    rows_by_tag("diffusion models")
    """
    conn = get_conn()
    q = f"%{keyword.lower()}%"
    return conn.execute(
        "SELECT title, authors, summary, published FROM papers "
        "WHERE LOWER(tags) LIKE ? ORDER BY published DESC LIMIT ?", (q, limit)
    ).fetchall()


    