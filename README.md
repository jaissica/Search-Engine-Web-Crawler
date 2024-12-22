# Search Engine Web Crawler

## Overview

The **Search Engine Web Crawler** is a Python-based web crawler designed to index and retrieve web documents using advanced information retrieval models such as BM25, TF-IDF, and language models (LM). The project integrates **Elasticsearch** for efficient data indexing and querying, and incorporates **pseudo-relevance feedback** to enhance search results. The crawler processes web data, applies various retrieval models, and provides functionalities for testing and training these models. 

## Key Components

### 1. Web Crawling and Data Parsing
- **`data_parser.py`**: Extracts and parses data from crawled web pages, processes HTML content, removes stop words, and prepares the data for indexing.
- **`parser.py`**: Handles different data formats and additional preprocessing steps needed during the parsing phase.

### 2. Indexing and Retrieval with Elasticsearch
- **`es.py`**: Main script for interacting with **Elasticsearch**, setting up connections, and handling basic indexing and querying operations.
- **`es_index_data.py`**: Responsible for indexing parsed documents into **Elasticsearch**, structuring the data into a format suitable for Elasticsearch indexing.
- **`es_retrieval_models.py`**: Implements retrieval models like **BM25**, **TF-IDF**, and **LM** over Elasticsearch, customizing Elasticsearch queries to apply these models and retrieve ranked lists of documents.

### 3. Information Retrieval Models
- **BM25**:
  - **`bm25_result.txt`**: Stores the results of the **BM25** retrieval model.
  - **`bm25_pseudo_rel_result.txt`** and **`bm25_pseudo_rel_result_es.txt`**: Results incorporating pseudo-relevance feedback to refine retrieval effectiveness.
- **Language Models (LM)**:
  - **`lmjm_result.txt`**: Results from a language model with **Jelinek-Mercer** smoothing.
  - **`lml_result.txt`**: Results from another variation of a language model.
- **TF-IDF**:
  - **`tfidf_result.txt`**: Results from the **TF-IDF** retrieval model.
- **Okapi TF**:
  - **`okapitf_result.txt`**: Stores results using the **Okapi TF** retrieval model.

### 4. Pseudo-Relevance Feedback
- **`pseudo_rel_feedback.py`**: Implements **pseudo-relevance feedback**, refining search results based on an initial round of retrieval.
- **`pseudo_rel_es.py`**: Applies **pseudo-relevance feedback** directly within Elasticsearch to improve search accuracy.

### 5. Evaluation and Testing
- **`qrels.adhoc.51-100.AP89.txt`**: A file containing relevance judgments used to evaluate the performance of the retrieval models.
- **`query_desc.51-100.short.txt`**: A set of queries used to test the retrieval models.
- **`results.xlsx`**: A spreadsheet containing detailed results and comparisons across different models and experiments.

### 6. Additional Scripts and Utilities
- **`main.py`**: The entry point for running the project, coordinating the crawling, indexing, and retrieval processes.
- **`stemming_ind.py`**: Handles stemming of words in the documents, possibly using predefined rules (`stem-classes.lst`).
- **`stoplist.txt`**: A list of stop words to be removed during the parsing process.
- **`term_vectors.json`**: A JSON file storing term vectors for documents, aiding in retrieval and ranking.

## How It Works

1. **Crawling and Parsing**: The project starts by crawling the web (if integrated with a crawler) and parsing the HTML content to extract relevant text data.
2. **Indexing**: Parsed data is indexed into **Elasticsearch**, where it is stored in a structured format suitable for retrieval.
3. **Retrieval Models**: Various retrieval models (BM25, TF-IDF, LM) are applied to the indexed data to retrieve and rank documents based on relevance to user queries.
4. **Pseudo-Relevance Feedback**: An initial round of retrieval is refined using pseudo-relevance feedback, improving the ranking of relevant documents.
5. **Evaluation**: The effectiveness of different models is evaluated using standard relevance judgments, and results are stored for comparison.

## Prerequisites

- **Python 3.x**
- **Elasticsearch**
- **Kibana** (optional, for visualization)
- **Python Libraries**: `elasticsearch`, `requests`, `BeautifulSoup`, `pandas`, `numpy`, `nltk`

## Installation

1. **Install Elasticsearch and Kibana**:
  - Follow the official installation guides for **Elasticsearch** and **Kibana**.
    - **Elasticsearch:** https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
    - **Kibana:** https://www.elastic.co/guide/en/kibana/index.html

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/jaissica/Search-Engine-Web-Crawler.git
   cd Search-Engine-Web-Crawler
   ```
3. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Elasticsearch:**
- Ensure Elasticsearch is running and update the connection settings in `es.py` or other relevant scripts.

## How to Run
1. **Index Data:**
- Use `es_index_data.py` to index the parsed data into Elasticsearch.
  ```bash
  python es_index_data.py
  ```
2. **Run Retrieval Models:**
- Execute `es_retrieval_models.py` or other relevant scripts to perform document retrieval.
  ```bash
  python es_retrieval_models.py
  ```
3. **Evaluate Results:**
- Compare the results stored in .txt files or results.xlsx to evaluate the effectiveness of different retrieval models.


