import ssl
from os.path import exists
from bs4 import BeautifulSoup as bs
import time
import urllib.robotparser
import json
import jsonpickle
from canonicalization import canonicalize
import queue
from urllib.parse import urlparse, urljoin
from urllib import request
from urllib.error import HTTPError
import requests





ssl._create_default_https_context = ssl._create_unverified_context
rp = urllib.robotparser.RobotFileParser()


#crawler Step 1
initial_seeds = [
   "http://en.wikipedia.org/wiki/Mitt_Romney",
    "http://en.wikipedia.org/wiki/Governorship_of_Mitt_Romney",
    "https://www.romney.senate.gov/biography/",
    "https://www.nga.org/governor/mitt-romney/"
]


def url_status_code(url):
    status = 200
    try:
        r = requests.get(url, timeout=(2, 20))
        return r.status_code
    except HTTPError as err:
        return 200
    except:
        return 401
    return status


ignore = {'facebook', 'gettyimages', 'video', 'image', 'job', 'password', 'privacy', 'terms', 'about us', '.mp4',
          'coronavirus', 'covid', ".jpg", ".jpeg", ".gif", ".png", ".pdf", ".php", ".ppt", ".doc","htm","xml",
       "romneytaxplan",'accesibility', 'coupons', 'blog', 'russia',"enjoy", 'ukraine', '.mp3', "licenses",".css", "services", "twitter", "search",
          ".json", "signup", '(',".asp", "comment", "slate", "reddit", "shop", "contact", "calculator", "saint"
          }


status_path = "./status.json"


if not exists(status_path):
    found_domain = set()
    disallowed = set()
    disallowed_domains = set()
    out_link_graph = {}
    in_link_graph = {}
    pq = []
    queue.put(pq)
    q = [canonicalize(lk) for lk in initial_seeds]
    for l in q:
        queue.push(pq, [-100000,l])
    visited = set(q)
    count = 0
else:
    f = open(status_path)
    parsed_state = json.load(f)
    found_domain = jsonpickle.decode(parsed_state["found_domain"])
    disallowed = jsonpickle.decode(parsed_state["disallowed"])
    disallowed_domains = jsonpickle.decode(parsed_state["disallowed_domains"])
    out_link_graph = jsonpickle.decode(parsed_state["out_link_graph"])
    in_link_graph = jsonpickle.decode(parsed_state["in_link_graph"])
    pq = parsed_state["pq"]
    visited = jsonpickle.decode(parsed_state["visited"])
    count = parsed_state["count"]


ignore_url = {
}
ignore_domain = {
}


url_score_words = {"mitt" : 3, "romney": 3, "businessman": 2, "lawyer" : 1, "politics" : 2, "massachusetts": 0.5, "bishop" : 2, "government":1,
                    "boston" : 0.5}
important_domains = {'.gov', '.com', '.net', '.org', '.co', '.edu'}



def url_fetch(link):

    pars = urlparse(link)
    curr_scheme, curr_domain, curr_path = pars.scheme, pars.netloc, pars.path
    if curr_domain in ["", " ", None]:
        return False,rp
    rp.set_url(urljoin(f"{curr_scheme}://{curr_domain}", 'robots.txt'))

    robo_url = urljoin(f"{curr_scheme}://{curr_domain}", 'robots.txt')
    if curr_domain not in found_domain:
        status = url_status_code(robo_url)
        found_domain.add(curr_domain)
        print(robo_url)
        if status == 200:

            try:
                site = urllib.request.urlopen(urllib.request.Request(robo_url, headers={'User-Agent': '*'}))
            except TimeoutError as e:
                found_domain.add(curr_domain)
            except:
                disallowed_domains.add(curr_domain)
                return False,rp


            try:
                result = site.read().decode()
            except:
                result = site.read().decode('0x8b')

            for line in result.split("\n"):
                line = line.strip()
                if line.startswith('Disallow'):
                    try:
                        disallowed.add(urljoin(f"{curr_scheme}://{curr_domain}", line.split(': ')[1].split(' ')[0]))
                    except:
                        continue

        elif status == 401 or status == 403:
            disallowed_domains.add(curr_domain)

    if link in disallowed or curr_domain in disallowed_domains:
        return False,rp
    return True,rp


def url_wait(rp):
    delay = rp.crawl_delay(useragent="*")
    if delay != None:
        time.sleep(delay+1)
    else:
        time.sleep(1)


def url_socre(inlink,link):
    score = 0
    for k in url_score_words.keys():
        if k in link:
            score -= url_score_words[k]

    for i in important_domains:
        if i in inlink:
            score-=1
        if i in link:
            score-=1

    if urlparse(inlink).netloc != urlparse(link).netloc:
        score-=1

    score += len(in_link_graph[link])

    return score


def create_url(link, path):
    ps = urlparse(link)
    return urljoin(f"{ps.scheme}://{ps.netloc}", path)


wo_write_text = ""
write_diff = 100
while count < 45000 and not len(pq) == 0:
    cur_link = queue.pop(pq)[1]
    if cur_link in ignore_url:
        continue
    if urlparse(cur_link).netloc in ignore_domain:
        continue


    fetch, rp = url_fetch(cur_link)
    flag_ig = False
    for ign in ignore:
        if ign in cur_link:
            flag_ig = True
            break
    if flag_ig:
        continue


    if not fetch:
        continue
    url_wait(rp)
    try:
        req = requests.get(cur_link)
    except:
        continue

    if req.status_code != 200:
        continue
    content_type = req.headers.get('content-type')
    if "htm" not in content_type:
        continue

    soup = bs(req.text, "html.parser")

    try:
        lang = soup.html["lang"]
        print(lang)
        if lang not in ['en', None, ''] and 'en' not in lang:
            continue
    except:
        pass





    para = soup.find_all("p")
    final_text = ""

    for p in para:
        pass
        final_text += p.text


    final_text = ' '.join(final_text.split('\n'))
    final_text = ' '.join(final_text.split())
    count+=1

    title = soup.find('title')
    if title == None or soup.find_all('a') == None:
        continue

    title = title.text

    current_text = ""
    links = []
    temp_links = []
    for link in soup.find_all('a'):
        try:
            link = link.get('href')
            if urlparse(link).netloc == '':
                link = create_url(cur_link, link)

            link = canonicalize(link)
            link = "http" + link.split("http")[-1]
            temp_links.append(link)
            if link in in_link_graph:
                in_link_graph[link].add(cur_link)
            else:
                in_link_graph[link] = {cur_link}
            if link in visited or link in disallowed or urlparse(link).netloc in disallowed_domains:
                continue
            visited.add(link)
        except:
            continue
        flag = False
        for ign in ignore:
            if ign in link:
                flag = True
                break
        if flag:
            continue

        queue.push(links, [url_socre(cur_link,link),link])
        visited.add(link)

    for i in links:
        queue.push(pq,i)
        visited.add(i[1])


    if cur_link in out_link_graph:
        pass
        out_link_graph[cur_link].union({i for i in temp_links})
    else:
        out_link_graph[cur_link] = {i for i in temp_links}


    current_text = "<DOC>\n"
    current_text += "<DOCNO>"+cur_link+"</DOCNO>\n"
    current_text += "<HEAD>"+title+"</HEAD>\n"
    current_text += "<TEXT>\n"
    current_text += final_text + "\n"
    current_text += "</TEXT>\n"
    current_text += "</DOC>\n"
    wo_write_text += current_text


    if len(pq) > 50000:
        pq = pq[:50000]



    if count%write_diff==0:
        with open('status.json', 'w') as out_file:
            json_data = {"found_domain" : jsonpickle.encode(found_domain),
                         "disallowed" : jsonpickle.encode(disallowed),
                         "disallowed_domains": jsonpickle.encode(disallowed_domains),
                         "out_link_graph" : jsonpickle.encode(out_link_graph),
                         "in_link_graph": jsonpickle.encode(in_link_graph),
                         "pq":pq,
                         "visited": jsonpickle.encode(visited),
                         "count" : count}
            json.dump(json_data, out_file, sort_keys = True, indent = 4,
                      ensure_ascii = False)

        with open('./Data/crawled_data_'+ str(count//write_diff) + '.txt',"w+") as write_file:
            write_file.write(wo_write_text)

        wo_write_text = ""


