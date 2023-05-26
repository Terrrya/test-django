import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from proxy.utils.parse_css import find_static_files_in_css


def modify_soup_links(
    soup: BeautifulSoup,
    element_name: str,
    url: str,
    attr_name: str,
    base_url: str,
) -> None:
    """Change url in attr for element in soup by element's name"""
    for elem in soup.find_all(element_name, **{attr_name: True}):
        if not elem[attr_name].startswith(url):
            elem[attr_name] = urljoin(url, elem[attr_name])

        resource_url = elem[attr_name]
        filename = resource_url.split("/")[-1]
        filepath = os.path.join(settings.STATIC_ROOT, filename)

        if not os.path.exists(filepath):
            response = requests.get(resource_url)
            if "css" in filepath:
                filenames = find_static_files_in_css(response.text)

                for filename_from_css in filenames:
                    file_from_css_url = urljoin(base_url, filename_from_css)
                    file_from_css_response = requests.get(file_from_css_url)
                    file_from_css_path = os.path.join(
                        settings.STATIC_ROOT, filename_from_css
                    )

                    if not os.path.exists(file_from_css_path):
                        with open(file_from_css_path, "wb") as f:
                            f.write(file_from_css_response.content)

            with open(filepath, "wb") as f:
                f.write(response.content)

        elem[attr_name] = filepath
