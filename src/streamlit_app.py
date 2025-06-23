"""
Streamlit app for the research assistant.

- Search: search arXiv by field
- Digest: generate a digest of the latest papers
- Ideate: generate project ideas

"""

import streamlit as st
import html as ihtml
from datetime import date
from config     import MAX_RESULTS
from scrape     import scrape
from summarise  import summarise_pending
from digest     import build_html
from ideate     import ideate_from_topic, ideate_from_ids
from helpers    import render_rows, rows_by_tag
from db         import get_conn
import os
import subprocess

def install(package):
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])

install("arxiv")

st.set_page_config(page_title="Literature Scout", layout="wide")
tab1, tab2, tab3 = st.tabs(["🔍 Search", "📑 Digest", "💡 Ideate"])


with tab1:
    st.header("Search & ingest papers")
    c1, c2, c3, c4 = st.columns(4)
    topic    = c1.text_input("Topic")
    title    = c2.text_input("Title")
    author   = c3.text_input("Author")
    category = c4.text_input("Category (e.g. cs.CL)")
    k = st.slider("Max papers", 5, 50, 25)
    if st.button("Run search"):
        scrape(max_results=k, topic=topic, title=title,
               author=author, category=category)
        st.success("Scraped, tagged, stored!")
        from db import get_conn
        newest = get_conn().execute(
            "SELECT title, authors, abstract, published FROM papers "
            "ORDER BY published DESC LIMIT ?", (k,)
        ).fetchall()
        st.components.v1.html(render_rows(newest), height=600, scrolling=True)

# ───────── TAB 2 – Digest (unchanged) ─────────────────────────────
with tab2:
    st.header("Digest from local DB")
    d_topic = st.text_input("Keyword to match tags", value="large language")
    if st.button("Generate digest"):
        summarise_pending()
        rows = rows_by_tag(d_topic, MAX_RESULTS)
        st.components.v1.html(render_rows(rows), height=800, scrolling=True)

# ───────── TAB 3 – Ideate (new feedback) ──────────────────────────
with tab3:
    st.header("Brainstorm new research ideas")
    mode = st.radio("Context source", ["Keyword", "ArXiv IDs"])

    if mode == "Keyword":
        kw = st.text_input("Keyword")
        if st.button("Ideate"):
            ideas = ideate_from_topic(kw)
            if ideas is None:
                st.info("No papers in the database match that keyword. "
                        "Try running a search in the **Search** tab first.")
            else:
                st.markdown(f"```\n{ideas}\n```")

    else:
        ids_in = st.text_area("Comma-separated IDs",
                              placeholder="2406.01234,2405.01234")
        if st.button("Ideate"):
            ids   = [x.strip() for x in ids_in.split(",") if x.strip()]
            ideas = ideate_from_ids(ids)
            if ideas is None:
                st.info("Those IDs aren’t in the database yet. "
                        "Fetch them via the **Search** tab, then try again.")
            else:
                st.markdown(f"```\n{ideas}\n```")
