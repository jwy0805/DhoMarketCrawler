class Post:
    def __init__(self, title, link):
        self.title = title
        self.link = link

class PostDetail:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

class Required:
    def __init__(self, sender, order, banned_authors):
        self.sender = sender
        self.order = order
        self.banned_authors = banned_authors

class Order:
    def __init__(self, keywords, label):
        self.keywords = keywords
        self.label = label

class LabeledText:
    def __init__(self, text, label):
        self.text = text
        self.label = label
