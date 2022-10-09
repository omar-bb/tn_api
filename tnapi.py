from __future__ import annotations
from bs4 import BeautifulSoup
from article import Article
import concurrent.futures
import requests
import json


class TNApiMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TNApi(metaclass=TNApiMeta):

    URL = "https://www.tunisienumerique.com/"

    @staticmethod
    def _make_soup(url: str) -> BeautifulSoup:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        return soup

    # static?
    def _format_to_json(self, articles: list[Article], ft_name="articles") -> str:
        articles = list(map(lambda x: x.__dict__, articles))  # type: ignore
        articles_dict = {ft_name: articles}

        return json.dumps(articles_dict, indent=4, ensure_ascii=False)

    def _get_article(self, url: str) -> Article:
        return Article.from_url(url)

    def _get_all_articles(self, urls: list[str]) -> list[Article]:
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for result in executor.map(self._get_article, urls):
                results.append(result)

        return results

    def get_top_48h(self) -> str:
        soup = self._make_soup(self.URL)
        div = soup.find_all("div", class_="feat-widget-cont left relative")[2]

        urls = [a["href"] for a in div.find_all("a")]

        top_48h_articles = self._get_all_articles(urls)
        return self._format_to_json(top_48h_articles, ft_name="top_48h_articles")

    def get_articles_highlights(self):
        soup = self._make_soup(self.URL)
        div = soup.find_all("div", class_="feat-widget-cont left relative")[0]
        div2 = soup.find_all("div", class_="blog-widget-wrap left relative")[0]

        urls = [a["href"] for a in div.find_all("a")] + [a["href"] for a in div2.find_all("a")]


