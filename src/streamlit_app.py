"""
Streamlit app for the research assistant.

- Search: search arXiv by field
- Digest: generate a digest of the latest papers
- Ideate: generate project ideas

"""
import pathlib, tempfile
import os
# set up for Hugging Face Spaces
CACHE_DIR = pathlib.Path(tempfile.gettempdir()) / "hf_cache"
os.environ["XDG_CACHE_HOME"] = str(pathlib.Path(tempfile.gettempdir()) / "hf_cache")
for var in (
    "HF_HOME",
    "HF_HUB_CACHE",
    "TRANSFORMERS_CACHE",
    "SENTENCE_TRANSFORMERS_HOME",
    "TRITON_CACHE_DIR",
):
    os.environ[var] = str(CACHE_DIR)
    
import streamlit as st
from datetime import date
from config     import MAX_RESULTS
from scrape     import scrape
from digest     import build_html
from ideate     import ideate_from_topic, ideate_from_ids
from helpers    import render_rows, rows_by_tag
from db         import get_conn
from summarise     import summarise_by_tag



st.set_page_config(page_title="Research Assistant", layout="wide")
tab1, tab2, tab3 = st.tabs(["🔍 Search", "📑 Digest", "💡 Ideate"])


with tab1:
    st.header("Search for papers you have not yet read")
    c1, c2, c3, c4 = st.columns(4)
    topic    = c1.text_input("Topic")
    title    = c2.text_input("Title")
    author   = c3.text_input("Author")
    category = c4.text_input("Category (e.g. cs.CL)")
    k = st.slider("Max papers", 5, 50, 25)
    if st.button("Run search"):
        with st.spinner("Finding new papers for your search..."):
            search_results = scrape(max_results=k, topic=topic, title=title,
               author=author, category=category)
        
        if search_results:
            st.success(f"Found {len(search_results)} new papers for your search!")
            # Convert search results to the format expected by render_rows
            paper_rows = [(p['title'], p['authors'], p['abstract'], p['published']) 
                         for p in search_results]
            st.components.v1.html(render_rows(paper_rows), height=600, scrolling=True)
        else:
            st.info("No new papers found for this search. All recent papers on this topic are already in your database.")


with tab2:
    st.header("Get a digest from the latest papers you have previously scraped")
    d_topic = st.text_input("Keyword to match tags", value="large language")
    if st.button("Generate digest"):
        with st.spinner("Finding papers and summarising them..."):
            summarise_by_tag(d_topic)
    rows = rows_by_tag(d_topic, MAX_RESULTS)
    if not rows:
        st.info("No papers found; try the Search tab.")
    else:
        st.components.v1.html(render_rows(rows), height=800, scrolling=True)

with tab3:
    st.header("Brainstorm new research ideas based on previously scraped papers")
    mode = st.radio("Context source", ["Keyword", "ArXiv IDs"])

    if mode == "Keyword":
        kw = st.text_input("Keyword")
        if st.button("Ideate"):
            with st.spinner("Thinking of new ideas..."):
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
            with st.spinner("Thinking of new ideas..."):
                ids   = [x.strip() for x in ids_in.split(",") if x.strip()]
                ideas = ideate_from_ids(ids)
            if ideas is None:
                st.info("Those IDs aren't in the database yet. "
                        "Fetch them via the Search tab, then try again.")
            else:
                st.markdown(f"```\n{ideas}\n```")
