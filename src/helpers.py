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
        #Handle None values by converting to empty strings
        title = html.escape(t) if t is not None else ""
        authors = html.escape(a) if a is not None else ""
        summary = html.escape(txt) if txt is not None else ""
        published = pub[:10] if pub is not None else ""
        
        blocks += [
            f"<h3>{title}</h3>",
            f"<p><b>Authors:</b> {authors} <br><i>{published}</i></p>",
            f"<pre style='white-space:pre-wrap'>{summary}</pre>",
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


    