from time import sleep
from src.crawler import get_board_links, crawl_detail_page

# links = get_board_links(1)
#
# sleep(1)

# post = crawl_detail_page(links[5])
post1 = crawl_detail_page("https://m.inven.co.kr/board/dho/533/1087188")
sleep(1)
post2 = crawl_detail_page("https://m.inven.co.kr/board/dho/533/1087419")

print(post1.title + "\n" + post1.author + "\n" + post1.content + "\n")
print(post2.title + "\n" + post2.author + "\n" + post2.content + "\n")
