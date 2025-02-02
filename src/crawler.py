import requests
from bs4 import BeautifulSoup
from data_model import Post, PostDetail, LabeledText
from analyzer import buy_keywords, sell_keywords, over_keywords, both_keywords

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

    reversed_post_list = list(reversed(post_list))
    return reversed_post_list

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

    main_text = "".join(content_tag.find_all(text=True, recursive=False)).strip()
    if main_text and len(main_text) < 50:
        lines.append(main_text.replace(" ", ""))

    for tag in content_tag.find_all(["div", "p", "br"], recursive=True):
        text = tag.get_text(separator=" ", strip=True)
        if text and len(text) < 50:
            lines.append(text.replace(" ", ""))

    return lines

def remove_server_tag_from_title(title_tag):
    if title_tag:
        span_tag = title_tag.select_one("span.in-cate")
        if span_tag:
            span_tag.decompose()

def label_each_text(content):
    labeled_text_list = []
    state = "none"

    for text in content:
        if any(keyword in text for keyword in buy_keywords):
            state = "buy"
            continue
        elif any(keyword in text for keyword in sell_keywords):
            state = "sell"
            continue
        else:
            if state == "buy":
                labeled_text = LabeledText(text, "buy")
            elif state == "sell":
                labeled_text = LabeledText(text, "sell")
            else:
                labeled_text = LabeledText(text, "none")

            labeled_text_list.append(labeled_text)

    return labeled_text_list