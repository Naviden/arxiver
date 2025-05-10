import streamlit as st
import feedparser
from urllib.parse import quote_plus
from datetime import datetime



# Define arXiv categories
arxiv_categories = {
    'Artificial Intelligence': 'cs.AI',
    'Computation and Language': 'cs.CL',
    'Computer Vision and Pattern Recognition': 'cs.CV',
    'Machine Learning': 'cs.LG',
    'Multiagent Systems': 'cs.MA',
    'Quantum Physics': 'quant-ph',
    'High Energy Physics - Theory': 'hep-th',
    'High Energy Physics - Experiment': 'hep-ex',
    'Mathematics': 'math',
    'Statistics': 'stat',
    'Electrical Engineering and Systems Science': 'eess',
    'Economics': 'econ'
}

# Function to build the arXiv query
def build_arxiv_query(include_terms=None, exclude_terms=None, start_date=None, end_date=None):
    query_parts = []

    # Include terms
    if include_terms:
        for field, terms in include_terms.items():
            for term in terms:
                term_quoted = f'"{term}"' if ' ' in term else term
                query_parts.append(f'{field}:{term_quoted}')

    # Exclude terms
    if exclude_terms:
        for field, terms in exclude_terms.items():
            for term in terms:
                term_quoted = f'"{term}"' if ' ' in term else term
                query_parts.append(f'ANDNOT {field}:{term_quoted}')

    # Date filter
    if start_date or end_date:
        # Format dates to YYYYMMDDHHMM
        start_str = start_date.strftime("%Y%m%d%H%M") if start_date else "000001010000"
        end_str = end_date.strftime("%Y%m%d%H%M") if end_date else "300001010000"
        date_query = f'submittedDate:[{start_str} TO {end_str}]'
        query_parts.append(date_query)

    # Combine all parts with AND
    combined_query = ' AND '.join(query_parts)
    return quote_plus(combined_query)

# Function to fetch papers from arXiv
def fetch_arxiv_papers(search_query, start_index=0, max_results=1000, sort_by='submittedDate', sort_order='descending'):
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query={search_query}&start={start_index}&max_results={max_results}&sortBy={sort_by}&sortOrder={sort_order}'
    feed = feedparser.parse(base_url + query)

    if feed.bozo:
        st.error(f"Failed to parse feed: {feed.bozo_exception}")
        return [], 0

    total_results = int(feed.feed.get('opensearch_totalresults', 0))

    papers = []
    for entry in feed.entries:
        paper = {
            'title': entry.get('title', 'No title'),
            'authors': ', '.join(author.name for author in entry.get('authors', [])),
            'published': entry.get('published', 'No publish date'),
            'summary': entry.get('summary', 'No summary'),
            'link': entry.get('link', 'No link')
        }
        papers.append(paper)

    return papers, total_results

# Streamlit app
def main():
    st.set_page_config(page_title="arXiv Paper Search", layout="wide")
    st.title("📚 arXiv Paper Search")

    st.sidebar.header("Search Filters")

    # Category filter moved to the top
    st.sidebar.subheader("Main Fields")
    selected_fields = st.sidebar.multiselect(
        "Select one or more fields of the paper",
        options=list(arxiv_categories.keys())
    )

    # Inclusion filters
    st.sidebar.subheader("Include Terms")
    include_title = st.sidebar.text_input("Title includes (comma-separated)", "")
    include_abstract = st.sidebar.text_input("Abstract includes (comma-separated)", "")
    include_author = st.sidebar.text_input("Author includes (comma-separated)", "")

    # Exclusion filters
    st.sidebar.subheader("Exclude Terms")
    exclude_title = st.sidebar.text_input("Title excludes (comma-separated)", "")
    exclude_abstract = st.sidebar.text_input("Abstract excludes (comma-separated)", "")
    exclude_author = st.sidebar.text_input("Author excludes (comma-separated)", "")

    # Date filters
    st.sidebar.subheader("Date Range")
    start_date = st.sidebar.date_input("Start date", value=None)
    end_date = st.sidebar.date_input("End date", value=None)

    # Search parameters
    st.sidebar.subheader("Search Parameters")
    num_display = st.sidebar.number_input("Number of results to display", min_value=1, max_value=100, value=10)
    sort_by = st.sidebar.selectbox("Sort by", options=['relevance', 'lastUpdatedDate', 'submittedDate'], index=2)
    sort_order = st.sidebar.selectbox("Sort order", options=['descending', 'ascending'], index=0)

    if st.sidebar.button("Search"):
        # Prepare inclusion and exclusion dictionaries
        include_terms = {}
        exclude_terms = {}

        if include_title:
            include_terms['ti'] = [term.strip() for term in include_title.split(',') if term.strip()]
        if include_abstract:
            include_terms['abs'] = [term.strip() for term in include_abstract.split(',') if term.strip()]
        if include_author:
            include_terms['au'] = [term.strip() for term in include_author.split(',') if term.strip()]

        if exclude_title:
            exclude_terms['ti'] = [term.strip() for term in exclude_title.split(',') if term.strip()]
        if exclude_abstract:
            exclude_terms['abs'] = [term.strip() for term in exclude_abstract.split(',') if term.strip()]
        if exclude_author:
            exclude_terms['au'] = [term.strip() for term in exclude_author.split(',') if term.strip()]

        # Add category filters
        if selected_fields:
            selected_categories = [arxiv_categories[field] for field in selected_fields]
            include_terms['cat'] = selected_categories

        # Build and execute query
        search_query = build_arxiv_query(include_terms=include_terms, exclude_terms=exclude_terms,
                                         start_date=start_date, end_date=end_date)
        papers, total_papers = fetch_arxiv_papers(search_query, start_index=0, max_results=1000, sort_by=sort_by, sort_order=sort_order)

        # Display total number of matched papers
        st.subheader(f"Total Papers Found: {total_papers}")

        # Display date range of retrieved papers
        if papers:
            # Extract publication dates
            pub_dates = [datetime.strptime(paper['published'], "%Y-%m-%dT%H:%M:%SZ") for paper in papers]
            min_date = min(pub_dates).date()
            max_date = max(pub_dates).date()
            st.markdown(f"**Date Range of Retrieved Papers:** {min_date} to {max_date}")
        else:
            st.warning("No papers found or failed to fetch data from arXiv API.")
            return

        # Display results
        for idx, paper in enumerate(papers[:num_display], start=1):
            st.markdown(f"### {idx}. {paper['title']}")
            st.markdown(f"**Authors:** {paper['authors']}")

            # Parse the published date string to a datetime object
            published_dt = datetime.strptime(paper['published'], "%Y-%m-%dT%H:%M:%SZ")

            # Format the datetime object to a date string
            published_date = published_dt.strftime("%Y-%m-%d")

            st.markdown(f"**Published:** {published_date}")
            st.markdown(f"**Link:** [arXiv]({paper['link']})")
            with st.expander("Abstract"):
                st.write(paper['summary'])
            st.markdown("---")

if __name__ == "__main__":
    main()