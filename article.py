from __future__ import annotations
from bs4 import BeautifulSoup
import requests
import re


class Article:
    """The article class"""

    def __init__(self, story, iconography, body_text, imgs=None) -> None:
        self.story = story
        self.iconography = iconography
        self.body_text = body_text
        if imgs is None:
            self.imgs = []
        else:
            self.imgs = imgs

    @classmethod
    def from_url(cls, url) -> Article:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        story = cls._get_article_story(soup)
        iconography = cls._get_article_iconography(soup)
        body_text = cls._get_article_body_text(soup)
        imgs = cls._get_article_imgs(soup)

        return cls(story, iconography, body_text, imgs)

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
    def _get_article_story(soup: BeautifulSoup) -> str:
        story = soup.find(
            "h1", class_="post-title entry-title left").text.strip()

        return story

    @staticmethod
    def _get_article_iconography(soup: BeautifulSoup) -> str:
        div = soup.find("div", id="post-feat-img")
        if div:
            iconography = div.find("img")["src"]
            return iconography
        div = soup.find("div", id="video-embed")
        iconography = div.find("iframe")["src"]

        return iconography

    @staticmethod
    def _get_article_body_text(soup: BeautifulSoup) -> str:
        div = soup.find("div", id="content-main")
        delimiters = div.find_all("div", class_="simplesocialbuttons")
        body_text = Article._get_tags_from_delimiters(delimiters)
        body_text = re.sub("\\s+", " ", body_text.text.strip())

        return body_text

    @staticmethod
    def _get_article_imgs(soup: BeautifulSoup) -> list[str]:
        div = soup.find("div", id="content-main")
        delimiters = div.find_all("div", class_="simplesocialbuttons")
        content_new = Article._get_tags_from_delimiters(delimiters)

        imgs = [x["src"] for x in content_new.find_all("img")]

        return imgs

    def __repr__(self) -> str:
        return f"Article('{self.story}', '{self.iconography}', '{self.body_text}', {self.imgs})"

    def __str__(self) -> str:
        return str(self.__dict__)
