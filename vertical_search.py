import sys
import streamlit as st
from elasticsearch import Elasticsearch
import urllib.parse
import json
sys.path.append('srcs')


index = 'mass_gov'
cloud_id ='Jaissica:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRhMThhYzg2Y2VlOGM0NjFmYjEwMDc1ZjE4OGJhNWNjNCQ0NzMyYTMwYzhiZmY0NDIzODVkZWI1YmNlYWEzZGUwMw=='
es = Elasticsearch(request_timeout =10000, cloud_id = cloud_id, http_auth = ('elastic', "h28reIPsar278BCOdUAtPMS3"))


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
    # sort popular tags
    sorted_tags = res['hits']['hits']

    #print(res)
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
    i=1
    count=0
    DocID=[]
    Grade=[]
    #st.write(load_css(), unsafe_allow_html=True)
    st.title('Vertical Search')
    search = st.text_input('Enter search words:')
    if search:
        results = index_search(es, index, search, None, 0, PAGE_SIZE)
        for result in results:
            if count<200:
                res = result['_source']
                res['url'] = result['_id']
                st.text(count)
                st.markdown(res['url'])
                DocID.append(res['url'])
                grade=st.radio('Relevance', ('very relevant','relevant','non relevant'),key=i)
                check={'very relevant': 2,
                       'relevant':1,
                'non relevant':0}
                i=i+1
                #for g in grade:
                rel=check.get(grade)
                print('rel',rel)
                Grade.append(rel)
            elif count==200:
                pass
            count=count+1
            #break
            print('Grade',Grade)
        if st.button('Submit'):
            qrel_dict = {"QueryID": search,
                         "AssessorID": "Jaissica",
                         "DocID": DocID,
                         "Grade": Grade
                         }
            with open('data/qrel3.json', 'a') as outfile:
                    json.dump(qrel_dict, outfile, indent=2)
        else:
            pass



if __name__ == '__main__':
    main()