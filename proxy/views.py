import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpRequest

from proxy.utils.change_elements import modify_soup_links


BASE_URL = "https://news.ycombinator.com"

EXT_CONTENT_TYPE = {
    "css": "text/css",
    "js": "application/javascript",
    "svg": "image/svg+xml",
    "ico": "image/x-icon",
}


def hacker_news_proxy(request: HttpRequest) -> HttpResponse:
    path = request.get_full_path()
    host = (
        request.build_absolute_uri("/")
        if "SERVER_NAME" in request.META.keys()
        else "http://127.0.0.1:8232"
    )
    url = urljoin(BASE_URL, path) if host not in path else path

    response = requests.get(url)

    for ext in EXT_CONTENT_TYPE.keys():
        if ext in path:
            with open(path, "r") as f:
                file = f.read()

            return HttpResponse(file, content_type=EXT_CONTENT_TYPE[ext])

    soup = BeautifulSoup(response.content, "html.parser")

    for element in soup.find_all(text=True):
        element.string.replace_with(
            re.sub(r"\b\w{6}\b", lambda word: word.group() + "™", element)
        )

    for element_name, attr_name in [
        ("img", "src"),
        ("script", "src"),
        ("link", "href"),
    ]:
        modify_soup_links(
            soup=soup,
            element_name=element_name,
            attr_name=attr_name,
            url=url,
            base_url=BASE_URL,
        )

    for elem in soup.find_all("a", href=True):
        if BASE_URL in elem["href"]:
            elem["href"] = elem["href"].replace(BASE_URL, host)

    return HttpResponse(str(soup))
