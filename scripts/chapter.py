from utils import to_title_format, remove_special_chars
from unidecode import unidecode
from unicodedata import normalize

class Chapter():

    def __init__(self, key, topic, articles_data):
        self.key = key
        self.topic = topic
        self.formatted_title = to_title_format(key)
        self.articles = self.process_articles(articles_data)


    def process_articles(self, articles_data):
        tree = []
        for key in articles_data:
            article = Article(key, articles_data[key])
            tree.append(article)
        return tree

    def process_blamed(self, blamed):
        current_article = None
        lines_for_article = []
        for commit, lines in blamed:
            for line in lines:
                if Chapter.is_article_title(line):
                    print(line)
                    if current_article:
                        current_article.blamed_lines = lines_for_article
                    current_article = self.get_article_by_markdown(line)
                    lines_for_article = []
                else:
                    lines_for_article.append((commit, line))
        current_article.blamed_lines = lines_for_article
                

    def get_article_by_markdown(self, markdown_line):
        article_key = remove_special_chars(markdown_line)
        article_key = article_key.replace('\xa0', ' ')
        article_key = article_key.replace('### ', '')
        article_key = article_key.replace('Artículo', '')
        article_key = article_key.replace('Articulo', '')
        article_key = article_key.strip()
        article_key = article_key.lower()

        def neutral_string(string):
            string = string.replace(' ', '').replace('_', '')
            return unidecode(string)

        for article in self.articles:
            if neutral_string(article.key) == neutral_string(article_key):
                return article

        raise ArticleNotFoundException(markdown_line, article_key)

    def is_article_title(title):
        norm_title = normalize('NFKD', title)
        return norm_title.strip().startswith(normalize('NFKD', '### '))



class Article():

    def __init__(self, key, article_data):
        self.key = str(key)
        self.formatted_title = to_title_format(key)
        self.topics = article_data['temas']
        self.blamed_lines = []


class ArticleNotFoundException(Exception):
    pass
