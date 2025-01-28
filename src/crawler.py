import requests
from bs4 import BeautifulSoup
import time

class Post:
    def __init__(self, title, author, content, content_html):
        self.title = title
        self.author = author
        self.content = content
        self.content_html = content_html


def get_board_links(page_num):
    url = f"https://m.inven.co.kr/board/dho/533?p={page_num}"  # 실제 목록 페이지 주소
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.select("section.mo-board-list ul li.list a.com-btn")

    links = []
    for link_tag in anchors:
        link = link_tag.get("href")
        pos = link.find("&c=")
        if pos != -1:
            link = link[:pos]

        links.append(link)

    return links

def crawl_detail_page(detail_url):
    response = requests.get(detail_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title = get_title(soup)
    author = get_author(soup)
    (content_text, content_html) = get_content(soup)
    return Post(title, author, content_text, content_html)

def get_title(soup):
    title_tag = soup.select_one("h2#articleSubject")
    remove_server_tag_from_title(title_tag)
    return title_tag.get_text(strip=True) if title_tag else ""

def get_author(soup):
    author_tag = soup.select_one("div#article-writer")
    return author_tag.get_text(strip=True) if author_tag else ""

def get_content(soup):
    content_tag = soup.select_one("div#imageCollectDiv")
    if not content_tag: return "", ""
    target_tag = content_tag.select_one("div#powerbbsContent") or content_tag

    lines = []

    if target_tag:
        for tag in target_tag.find_all("div", recursive=False):
            text = tag.get_text(strip=True)
            html = str(tag)
            if text:
                lines.append((text, html))
    else:
        raw_text = content_tag.get_text("\n", strip=True)
        raw_html = str(content_tag)
        for line in raw_text.split("\n"):
            if line.strip():
                lines.append((line.strip(), raw_html))

    content_text = "\n".join(line[0] for line in lines)
    content_html = "\n".join(line[1] for line in lines)

    return content_text, content_html

def remove_server_tag_from_title(title_tag):
    if title_tag:
        span_tag = title_tag.select_one("span.in-cate")
        if span_tag:
            span_tag.decompose()