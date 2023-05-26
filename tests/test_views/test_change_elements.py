import os
from unittest.mock import patch, Mock

from bs4 import BeautifulSoup
from django.conf import settings
from django.test import TestCase

from proxy.utils.change_elements import modify_soup_links


@patch("proxy.utils.change_elements.requests.get")
class ChangeElementsTests(TestCase):
    def setUp(self) -> None:
        page = (
            "<html>"
            "<head>"
            "<link href='test.css'></link>"
            "</head>"
            "<body>"
            "<img src='image.jpg'></img>"
            "<a href='https://testlink.com'>test link</a>"
            "<script src='test.js'></script>"
            "</body>"
            "</html>"
        )
        self.soup = BeautifulSoup(page, "html.parser")
        self.url = "https://test.com"

    def test_change_elements_modify_img_urls(
        self, mock_response: Mock
    ) -> None:
        img_urls = os.path.join(settings.STATIC_ROOT, "image.jpg")
        mock_response.return_value = ""

        modify_soup_links(
            soup=self.soup,
            element_name="img",
            attr_name="src",
            url=self.url,
            base_url="",
        )
        modified_img_url = self.soup.find("img", src=True)["src"]
        self.assertEqual(img_urls, modified_img_url)

    @patch("proxy.utils.change_elements.find_static_files_in_css")
    def test_change_elements_modify_css_urls(
        self, mock_response: Mock, mock_filenames: Mock
    ) -> None:
        css_url = os.path.join(settings.STATIC_ROOT, "test.css")
        mock_response.return_value = ""
        mock_filenames.return_value = b""

        modify_soup_links(
            soup=self.soup,
            element_name="link",
            attr_name="href",
            url=self.url,
            base_url="",
        )
        modified_css_url = self.soup.find("link", href=True)["href"]
        self.assertEqual(css_url, modified_css_url)

    def test_change_elements_modify_js_urls(self, mock_response: Mock) -> None:
        js_url = os.path.join(settings.STATIC_ROOT, "test.js")
        mock_response.return_value = ""

        modify_soup_links(
            soup=self.soup,
            element_name="script",
            attr_name="src",
            url=self.url,
            base_url="",
        )
        modified_js_url = self.soup.find("script", src=True)["src"]
        self.assertEqual(js_url, modified_js_url)

    def test_change_elements_not_modify_another_urls(
        self, mock_response: Mock
    ) -> None:
        a_url = "https://testlink.com"
        mock_response.return_value = ""

        for element_name, attr_name in [
            ("img", "src"),
            ("script", "src"),
            ("link", "href"),
        ]:
            modify_soup_links(
                soup=self.soup,
                element_name=element_name,
                attr_name=attr_name,
                url=self.url,
                base_url="",
            )
        modified_a_url = self.soup.find("a", href=True)["href"]
        self.assertEqual(a_url, modified_a_url)
