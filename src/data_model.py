class Required:
    def __init__(self, sender, order, banned_authors):
        self.sender = sender
        self.order = order
        self.banned_authors = banned_authors

class Order:
    def __init__(self, keywords, label):
        self.keywords = keywords
        self.label = label

class