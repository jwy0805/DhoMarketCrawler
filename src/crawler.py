import requests
from bs4 import BeautifulSoup

class Post:
    def __init__(self, title, link):
        self.title = title
        self.link = link

class PostDetail:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

def get_board_links(page_num):
    url = f"https://m.inven.co.kr/board/dho/533?p={page_num}"  # 실제 목록 페이지 주소
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.select("section.mo-board-list ul li.list div.li-wrap")

    links = []
    for link_tag in anchors:
        link = link_tag.get("href")
        links.append(link)

    return links

def get_new_post_links(last_title=""):
    url = "https://m.inven.co.kr/board/dho/533"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    post_list = []
    for li in soup.select("section.mo-board-list ul li.list"):
        link_tag = li.select_one("div.li-wrap a.contentLink")
        title_tag = li.select_one("div.tit span.subject")

        if link_tag and title_tag:
            link = link_tag.get("href")
            title = title_tag.get_text(strip=True)

            if title == last_title or len(post_list) > 20:
                break

            post = Post(title, link)
            post_list.append(post)

    reversed_list = list(reversed(post_list))
    return reversed_list

def crawl_detail_page(detail_url):
    response = requests.get(detail_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title = get_title(soup)
    author = get_author(soup)
    content_text = get_content(soup)
    return PostDetail(title, author, content_text)

def get_title(soup):
    title_tag = soup.select_one("h2#articleSubject")
    remove_server_tag_from_title(title_tag)
    return title_tag.get_text(strip=True) if title_tag else ""

def get_author(soup):
    author_tag = soup.select_one("div#article-writer")
    return author_tag.get_text(strip=True) if author_tag else ""

def get_content(soup):
    content_tag = soup.select_one("div#imageCollectDiv")
    if not content_tag:
        return ""

    lines = []

    main_text = content_tag.get_text(separator=" ", strip=True)
    if main_text:
        lines.append(main_text)

    for tag in content_tag.find_all(["div", "p", "br"], recursive=True):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            lines.append(text)
    return lines

def remove_server_tag_from_title(title_tag):
    if title_tag:
        span_tag = title_tag.select_one("span.in-cate")
        if span_tag:
            span_tag.decompose()