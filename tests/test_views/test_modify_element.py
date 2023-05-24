from bs4 import BeautifulSoup
from django.test import TestCase

from proxy.views import modify_element


class ChangeElementsTests(TestCase):
    def setUp(self) -> None:
        page = (
            "<html>"
            "<head>"
            "</head>"
            "<body>"
            "<div>1234 123456 12345 1234567<div>"
            "</body>"
            "</html>"
        )
        self.soup = BeautifulSoup(page, "html.parser")

    def test_modify_element_add_symbol_to_word_with_six_letters(self) -> None:
        expected_text = "1234 123456™ 12345 1234567"
        element = self.soup.find(text=True)

        modify_element(element)
        actual_text = self.soup.find(text=True)

        self.assertEqual(expected_text, actual_text)
