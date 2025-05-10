# 📚 arXiv Paper Search App

A user-friendly Streamlit web application to search and filter scientific papers from [arXiv.org](https://arxiv.org) using the official arXiv API. This tool allows researchers and enthusiasts to efficiently find papers based on various criteria.

## 🚀 Features

- **Multiple Field Selection**: Filter papers by selecting one or more arXiv categories (e.g., Artificial Intelligence, Quantum Physics).
- **Keyword Inclusion/Exclusion**: Include or exclude specific terms in the title, abstract, or author fields.
- **Date Range Filtering**: Search for papers published within a specific date range.
- **Result Limiting**: Specify the number of results to display.
- **Sorting Options**: Sort results by relevance, last updated date, or submission date.
- **Detailed Paper Information**: View each paper's title, authors, publication date, abstract, and a direct link to the arXiv page.
- **Date Range Display**: After performing a search, the app displays the range of publication dates for the retrieved papers.

## 🖥️ Live Demo

Access the live application here: [https://arxiv-checker.streamlit.app/](https://arxiv-checker.streamlit.app/)


## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/arxiv-paper-search-app.git
   cd arxiv-paper-search-app
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```


## 📄 Requirements

- Python 3.7 or higher
- Packages listed in `requirements.txt`, including:
  - streamlit
  - feedparser
