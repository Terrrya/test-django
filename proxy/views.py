from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpRequest

BASE_URL = "https://news.ycombinator.com"


def check_word(word: str) -> bool:
    """Check that the word consists exactly of 6 letters"""
    if len(word) == 6 and word[-1] not in (",", ".", "!", "?", ":", ";"):
        return True
    return False


def add_spaces(element: BeautifulSoup, words: list[str]) -> None:
    """Add space to the first or to the last word if element has space in the
    start or in the end of element"""
    if element[0] == " ":
        words[0] = " " + words[0]
    if element[-1] == " ":
        words[-1] += " "


def change_elements(
    soup: BeautifulSoup, element_name: str, url: str, attr_name: str
) -> None:
    """Change url in attr for element in soup by element's name"""
    for elem in soup.find_all(element_name, **{attr_name: True}):
        elem[attr_name] = urljoin(url, elem[attr_name])


def modify_element(element: BeautifulSoup) -> BeautifulSoup:
    """Modify the element by adding "™" to words that have 6 letters"""
    words = element.split()
    if words:
        modified_words = [
            word + "™" if check_word(word) else word for word in words
        ]
        add_spaces(element, modified_words)
        element.string.replace_with(" ".join(modified_words))


def hacker_news_proxy(request: HttpRequest) -> HttpResponse:
    url = urljoin(BASE_URL, request.get_full_path())

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for element in soup.find_all(text=True):
        modify_element(element)

    for element_name, attr_name in [
        ("img", "src"),
        ("script", "src"),
        ("link", "href"),
    ]:
        change_elements(
            soup=soup, element_name=element_name, attr_name=attr_name, url=url
        )

    return HttpResponse(soup)
