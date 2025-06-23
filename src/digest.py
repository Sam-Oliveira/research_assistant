import datetime, html
from db import get_conn

"""
Build an HTML digest of the latest papers.

Example:
build_html(lookback_hours=48)
"""

def build_html(lookback_hours=48):
    today = datetime.date.today().isoformat()
    since = (datetime.datetime.utcnow() -
             datetime.timedelta(hours=lookback_hours)).isoformat()

    conn = get_conn()
    rows = conn.execute(
        "SELECT title, authors, summary, published "
        "FROM papers WHERE published >= ? "
        "ORDER BY published DESC", (since,)
    )

    out = [
        "<!DOCTYPE html>",
        "<meta charset='utf-8'>",
        f"<h1>Literature Digest — {today}</h1>",
        "<style>body{font-family:Arial,Helvetica,sans-serif;max-width:760px;margin:0 auto}</style>"
    ]
    for title, authors, summary, pub in rows:
        out += [
            f"<h2>{html.escape(title)}</h2>",
            f"<p><b>Authors:</b> {html.escape(authors)}<br><i>{pub[:10]}</i></p>",
            f"<pre style='white-space:pre-wrap'>{html.escape(summary)}</pre>",
            "<hr>"
        ]
    return "\n".join(out)