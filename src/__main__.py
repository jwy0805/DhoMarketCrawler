import time
from email.policy import default
from itertools import count
from time import sleep
from src.crawler import get_board_links, crawl_detail_page, get_new_post_links, get_title
from src.analyzer import get_post_type
from collections import Counter, defaultdict
import random

from src.data_model import Order, Required

required_list = [
    Required(
        "177328",
        [Order(["개나갤", "스스"], "sell"), Order(["개개오갤"], "sell")],
        ["흰살모사", "Meteoroid"]
    ),
    Required(
        "177330",
        [Order(["로라모"], "sell")],
        []
    ),
    Required(
        "177332",
        [Order(["ㄷㅋ"], "sell")],
        ["아기사탕"]
    )
]

last_title = "개장네바 증서 300억 팝니다(10숲)"

posts = get_new_post_links(last_title)
print(len(posts))

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

                if any(all(keyword in text for keyword in keywords) for text in [post_detail.title] + post_detail.content):
                    print(sender + " " + post.link)
                    print(post_detail.title)
                    print(post_detail.author)
                    print(post_detail.content)
                    print("===")
                    break

        elif post_type == "both":
            for sender, banned_authors, keyword in order_dict["both"]:
                if post_detail.author in banned_authors:
                    continue







# while True:
#     posts = get_new_post_links(last_title)
#     print(len(posts))
#
#     if len(posts) > 0 :
#         for post in posts:
#             last_title = post.title
#             sleep(1)
#             post_detail = crawl_detail_page(post.link)
#             post_type = get_post_type(post_detail.title)
#
#             if post_type == label and post_detail.author not in banned_authors:
#                 for line in post_detail.content:
#                     if any(keyword in line for keyword in keywords):
#                         print(post_detail.title)
#                         print(post_detail.author)
#                         print(post_detail.content)
#                         print("===")
#                         break
#
#
#     time.sleep(9)



# l = []
# content_lines = set()
# for page_num in range(1, 15):
#     links = get_board_links(page_num)
#     sleep(1)
#
#     for link in links:
#         post = crawl_detail_page(link)
#         post_type = get_post_type(post.title)
#
#         if post_type == "none" or post_type == "both" :
#             for line in post.content:
#                 content_lines.add(line)
#
#         t = random.uniform(0.5, 1.1)
#         sleep(t)