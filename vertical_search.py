import sys
import streamlit as st
from elasticsearch import Elasticsearch
import urllib.parse
sys.path.append('srcs')


index = 'mass_gov'
cloud_id ='9b1128ec78574fcd91ae19ac14496c8b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRjYzY0MmMyMjQxNmQ0NzVjYmI1OTdiZmJiMjFmNTlhNCQ4ZjkxY2UzNjVlODk0NWVkYjc2YmY0NDQzZTMwMjhlNg=='
es = Elasticsearch(request_timeout =10000, cloud_id = cloud_id, http_auth = ('elastic', "rFE1RkD1dJr54MPCtHaFHqub"))

PAGE_SIZE=5


def index_search(es, index: str, keywords: str, filters: str,
                 from_i: int, size: int) -> dict:
    """
    Args:
        es: Elasticsearch client instance.
        index: Name of the index we are going to use.
        keywords: Search keywords.
        filters: Tag name to filter medium stories.
        from_i: Start index of the results for pagination.
        size: Number of results returned in each search.
    """

    # search query
    body = {
            "size": 1000,
            "query": {
                "match": {"content": keywords
                          }
            }
        }

    res = es.search(index=index, body=body)
    sorted_tags = res['hits']['hits']
    return res['hits']['hits']


def load_css() -> str:
    """ Return all css styles. """
    common_tag_css = """
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: .15rem .40rem;
                position: relative;
                text-decoration: none;
                font-size: 95%;
                border-radius: 5px;
                margin-right: .5rem;
                margin-top: .4rem;
                margin-bottom: .5rem;
    """
    return f"""
        <style>
            #tags {{
                {common_tag_css}
                color: rgb(88, 88, 88);
                border-width: 0px;
                background-color: rgb(240, 242, 246);
            }}
            #tags:hover {{
                color: black;
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
            #active-tag {{
                {common_tag_css}
                color: rgb(246, 51, 102);
                border-width: 1px;
                border-style: solid;
                border-color: rgb(246, 51, 102);
            }}
            #active-tag:hover {{
                color: black;
                border-color: black;
                background-color: rgb(240, 242, 246);
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
        </style>
    """

def number_of_results(total_hits: int, duration: float) -> str:
    """ HTML scripts to display number of results and duration. """
    return f"""
        <div style="color:grey;font-size:95%;">
            {total_hits} results ({duration:.2f} seconds)
        </div><br>
    """

def search_result(i: int, url: str, title: str, highlights: str,
                  author: str, length: str, **kwargs) -> str:
    """ HTML scripts to display search results. """
    return f"""
        <div style="font-size:120%;">
            {i + 1}.
            <a href="{url}">
                {title}
            </a>
        </div>
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                {url[:90] + '...' if len(url) > 100 else url}
            </div>
            <div style="float:left;font-style:italic;">
                {author} ·&nbsp;
            </div>
            <div style="color:grey;float:left;">
                {length} ...
            </div>
            {highlights}
        </div>
    """

def tag_boxes(search: str, tags: list, active_tag: str) -> str:
    """ HTML scripts to render tag boxes. """
    html = ''
    search = urllib.parse.quote(search)
    for tag in tags:
        if tag != active_tag:
            html += f"""
            <a id="tags" href="?search={search}&tags={tag}">
                {tag.replace('-', ' ')}
            </a>
            """
        else:
            html += f"""
            <a id="active-tag" href="?search={search}">
                {tag.replace('-', ' ')}
            </a>
            """
    html += '<br><br>'
    return html


def main():
    st.title('Vertical Search')
    search = st.text_input('Enter search words:')
    if search:
        results = index_search(es, index, search, None, 0, PAGE_SIZE)
        total_hits = results
        for result in results:
            res = result['_source']
            res['url'] = result['_id']
            st.markdown(res['url'])
            st.markdown(res['content'])

if __name__ == '__main__':
    main()