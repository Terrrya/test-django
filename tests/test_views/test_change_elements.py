from bs4 import BeautifulSoup
from django.test import TestCase

from proxy.views import change_elements


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
        self.url = "https://test.com/"

    def test_change_elements_modify_img_urls(self) -> None:
        img_urls = "https://test.com/image.jpg"

        change_elements(
            soup=self.soup, element_name="img", attr_name="src", url=self.url
        )
        modified_img_url = self.soup.find("img", src=True)["src"]
        self.assertEqual(img_urls, modified_img_url)

    def test_change_elements_modify_css_urls(self) -> None:
        css_url = "https://test.com/test.css"

        change_elements(
            soup=self.soup, element_name="link", attr_name="href", url=self.url
        )
        modified_css_url = self.soup.find("link", href=True)["href"]
        self.assertEqual(css_url, modified_css_url)

    def test_change_elements_modify_js_urls(self) -> None:
        js_url = "https://test.com/test.js"

        change_elements(
            soup=self.soup,
            element_name="script",
            attr_name="src",
            url=self.url,
        )
        modified_js_url = self.soup.find("script", src=True)["src"]
        self.assertEqual(js_url, modified_js_url)

    def test_change_elements_not_modify_another_urls(self) -> None:
        a_url = "https://testlink.com"

        for element_name, attr_name in [
            ("img", "src"),
            ("script", "src"),
            ("link", "href"),
        ]:
            change_elements(
                soup=self.soup,
                element_name=element_name,
                attr_name=attr_name,
                url=self.url,
            )
        modified_a_url = self.soup.find("a", href=True)["href"]
        self.assertEqual(a_url, modified_a_url)
