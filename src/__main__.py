import itertools
import time
from email.policy import default
from itertools import count
from time import sleep
from src.crawler import crawl_detail_page, get_new_post_links, get_title, label_each_text
from src.analyzer import get_post_type
from collections import Counter, defaultdict
from data_model import Post
import random

from src.data_model import Order, Required

required_list = [
    Required(
        "177328",
        [Order(["개윈잼"], "sell"), Order(["개개오갤"], "sell")],
        ["흰살모사", "Meteoroid"]
    ),
    Required(
        "177330",
        [Order(["물방울"], "sell")],
        []
    ),
    Required(
        "177332",
        [Order(["ㄷㅋ"], "buy")],
        ["아기사탕"]
    )
]

last_title = "선박,장비,비전가이아상 ㅍㅍ"

posts = get_new_post_links(last_title)
# post = Post("", "https://m.inven.co.kr/board/dho/533/1087649")
# posts = [post]

if len(posts) > 0 :
    last_title = posts[0].title

    order_dict = defaultdict(list)
    for required in required_list:
        for order in required.order:
            order_dict[order.label].append((required.sender, required.banned_authors, order.keywords))

    for post in posts:
        time.sleep(1)
        post_detail = crawl_detail_page(post.link)
        post_type = get_post_type(post_detail.title)

        # order_dict 에서 해당 post_type 에 해당하는 order 만 조회
        if post_type in order_dict:
            for sender, banned_authors, keywords in order_dict[post_type]:
                if post_detail.author in banned_authors:
                    continue

                matched_keywords = []
                for keyword in keywords:
                    if any(keyword in text for text in [post_detail.title] + post_detail.content):
                        matched_keywords.append(keyword)

                if matched_keywords:
                    print(sender + " " + post.link + " : ".join(matched_keywords))
                    print(post_detail.title)
                    print(post_detail.author)
                    print(post_detail.content)
                    print("===")
                    break

        elif post_type == "both":
            labeled_text_list = label_each_text(post_detail.content)

            for trade_type in ["sell", "buy"]:
                for sender, banned_authors, keywords in order_dict.get(trade_type, []):
                    if post_detail.author in banned_authors:
                        continue

                    if any(labeled_text.label == trade_type and
                           any(keyword in labeled_text.text for keyword in keywords)
                           for labeled_text in labeled_text_list):
                                print(f"{sender} {post.link} : {', '.join(keywords)}")
                                print(post_detail.title)
                                print(post_detail.author)
                                print(post_detail.content)
                                print("===")
                                break