from __future__ import annotations
from bs4 import BeautifulSoup
import requests
import re


class Article:
    """The article class"""

    def __init__(self, title, content, imgs=None) -> None:
        self.title = title
        self.content = content
        if imgs is None:
            self.imgs = []
        else:
            self.imgs = imgs

    @classmethod
    def from_url(cls, url) -> Article:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        title = cls._get_article_title(soup)
        content = cls._get_article_content(soup)
        imgs = cls._get_article_imgs(soup)

        return cls(title, content, imgs)

    @staticmethod
    def _get_tags_from_delimiters(
            delimiters: list[BeautifulSoup]) -> BeautifulSoup:
        content = u""
        for tag in delimiters[0].next_siblings:
            if tag == delimiters[1]:
                break
            else:
                content += str(tag)
        content_new = BeautifulSoup(content.strip(), "html.parser")

        return content_new

    @staticmethod
    def _get_article_title(soup: BeautifulSoup) -> str:
        title = soup.find(
            "h1", class_="post-title entry-title left").text.strip()

        return title

    @staticmethod
    def _get_article_content(soup: BeautifulSoup) -> str:
        div = soup.find("div", id="content-main")
        delimiters = div.find_all("div", class_="simplesocialbuttons")
        content = Article._get_tags_from_delimiters(delimiters)
        content = re.sub("\\s+", " ", content.text.strip())

        return content

    @staticmethod
    def _get_article_imgs(soup: BeautifulSoup) -> list[str]:
        div = soup.find("div", id="content-main")
        delimiters = div.find_all("div", class_="simplesocialbuttons")
        content_new = Article._get_tags_from_delimiters(delimiters)

        imgs = [x["src"] for x in content_new.find_all("img")]

        return imgs

    def __repr__(self) -> str:
        return f"Article('{self.title}', '{self.content}', {self.imgs})"

    def __str__(self) -> str:
        return str(self.__dict__)


if __name__ == "__main__":
    article = Article.from_url(
        "https://sport.tunisienumerique.com/sport-tunisien-programme-tv-des-matches-de-dimanche-3/")
    print(str(article))
