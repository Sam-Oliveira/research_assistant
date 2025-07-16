

# Research Assistant

A Streamlit-based web application that helps researchers discover, digest, and ideate from arXiv papers using AI-powered tools.

## Overview

This research assistant provides three main functionalities through an intuitive web interface:

1. **🔍 Search**: Find and scrape new papers from arXiv
2. **📑 Digest**: Generate AI-powered summaries of previously scraped papers
3. **💡 Ideate**: Brainstorm new research ideas based on existing papers

## Features

### 🔍 Search Tab
The Search tab allows you to discover new papers from arXiv that you haven't read yet.

**How it works:**
- **Topic**: Search for papers containing specific topics in their content
- **Title**: Search for papers with specific words in their titles
- **Author**: Find papers by specific authors
- **Category**: Filter by arXiv categories (e.g., `cs.CL` for NLP, `cs.AI` for AI)
- **Max Papers**: Adjust the number of results (5-50 papers)

**What happens when you search:**
1. The app queries arXiv using your criteria
2. Automatically extracts keywords from titles and abstracts using KeyBERT
3. Stores new papers in a local SQLite database (avoiding duplicates)
4. Displays results in a clean, scrollable format

**Example searches:**
- Topic: "large language models", Category: "cs.CL"
- Author: "Geoffrey Hinton", Max Papers: 10
- Title: "transformer", Topic: "attention mechanisms"

### 📑 Digest Tab
The Digest tab provides AI-powered summaries of papers you've previously scraped.

**How it works:**
- **Keyword Matching**: Enter a keyword to find papers whose tags match your interest
- **AI Summarization**: Uses a fine-tuned LLaMA model to generate bullet-point summaries
- **Smart Filtering**: Only summarizes papers that haven't been summarized yet

**What you get:**
- Concise bullet-point summaries highlighting methods and key findings
- Papers organized by publication date
- Clean HTML rendering with titles, authors, and publication dates

**Example usage:**
- Keyword: "large language" → Gets all papers tagged with language model keywords
- Keyword: "diffusion" → Summarizes papers about diffusion models

### 💡 Ideate Tab
The Ideate tab helps you brainstorm new research ideas based on existing papers.

**Two modes available:**

1. **Keyword Mode:**
   - Enter a keyword to find relevant papers in your database
   - AI generates three new research project ideas based on those papers
   - Each idea includes title, motivation, method, and evaluation approach

2. **ArXiv IDs Mode:**
   - Provide specific arXiv paper IDs (comma-separated)
   - AI analyzes those specific papers to generate research ideas
   - Useful when you want to build upon particular papers

**What you get:**
- Three detailed research project proposals
- Each proposal includes:
  - Project title
  - Motivation and background
  - Proposed methodology (2 sentences)
  - Evaluation method

## Technical Overview

### Core Components

- **`streamlit_app.py`**: Main web interface with three tabs
- **`scrape.py`**: arXiv paper scraping with duplicate detection
- **`digest.py`**: HTML digest generation
- **`ideate.py`**: AI-powered research idea generation
- **`summarise.py`**: LLM-based paper summarization
- **`db.py`**: SQLite database management
- **`helpers.py`**: Utility functions for rendering and data retrieval
- **`query_builder.py`**: arXiv search query construction
- **`category_explorer.py`**: arXiv category utilities

### AI Models Used

- **KeyBERT + Sentence Transformers**: For keyword extraction from papers
- **LLaMA-3-8B-Instruct**: For generating summaries and research ideas
- **all-MiniLM-L6-v2**: For semantic similarity and keyword extraction

### Database Schema

The SQLite database stores papers with the following structure:
- `id`: arXiv paper ID (primary key)
- `title`: Paper title
- `authors`: Author names (comma-separated)
- `abstract`: Paper abstract
- `published`: Publication date
- `summary`: AI-generated summary (nullable)
- `tags`: Extracted keywords (comma-separated)

## Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### Dependencies
```
streamlit
arxiv
transformers
accelerate
bitsandbytes
torch
feedparser
sqlite-utils
fastapi
uvicorn
tiktoken
keybert
sentence-transformers
scikit-learn
```

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd research_assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run src/streamlit_app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

### Docker Deployment

The application includes a Dockerfile for containerized deployment:

```bash
docker build -t research-assistant .
docker run -p 8501:8501 research-assistant
```

## Usage Workflow

### Typical Research Workflow

1. **Start with Search**: Use the Search tab to find papers in your area of interest
   - Try different combinations of topic, author, and category filters
   - Start with 10-15 papers to build your database

2. **Generate Digests**: Switch to the Digest tab to get AI summaries
   - Use keywords that match your research interests
   - Review the bullet-point summaries to quickly understand key findings

3. **Brainstorm Ideas**: Use the Ideate tab to generate new research directions
   - Start with keyword mode to explore broad areas
   - Use specific arXiv IDs when you want to build upon particular papers

### Tips for Effective Use

- **Search Strategy**: Use specific categories (e.g., `cs.CL` for NLP) to get more targeted results
- **Keyword Selection**: Use the same keywords across tabs for consistency
- **Database Building**: The more papers you scrape, the better your digests and ideation will be
- **Iterative Process**: Use the ideation results to inform new searches

## Configuration

### Model Settings
- **Default Model**: `unsloth/llama-3-8b-Instruct-bnb-4bit`
- **Max Results**: 10 papers per search (configurable)
- **Database**: SQLite file stored in temporary directory

### Customization
Edit `src/config.py` to modify:
- Maximum search results
- AI model selection
- Database location

## Limitations

- **arXiv Rate Limiting**: The app respects arXiv's rate limits (1 second between requests)
- **Model Size**: Uses 8B parameter model for summarization and ideation
- **Local Storage**: Papers are stored locally in SQLite database
- **Internet Required**: Requires internet connection for arXiv queries and model downloads


## License

The open source version of this project is licensed under the GPLv3 license, which can be seen in the [LICENSE](LICENSE) file.
