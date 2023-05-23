from bs4 import BeautifulSoup
from django.test import TestCase

from proxy.views import add_spaces


class AddSpacesTests(TestCase):
    def setUp(self) -> None:
        page = (
            "<html>"
            "<head>"
            "<title>"
            "Test text with no spaces at the beginning and at the end"
            "</title>"
            "</head>"
            "<body>"
            "<div>test with spaces at the end </div>"
            "<div> test with spaces at the begin</div>"
            "<div> test with spaces at the begin and at the end </div>"
            "</body>"
            "</html>"
        )
        self.soup = BeautifulSoup(page)
        self.elements = self.soup.find_all(text=True)

    def test_add_spaces_do_nothing_if_no_spaces_begin_end(self) -> None:
        words = self.elements[0].split()
        add_spaces(self.elements[0], words)
        modify_string = " ".join(words)

        self.assertEqual(self.elements[0].string, modify_string)

    def test_add_spaces_add_space_if_space_at_the_end(self) -> None:
        words = self.elements[1].split()
        add_spaces(self.elements[1], words)
        modify_string = " ".join(words)

        self.assertEqual(self.elements[1].string, modify_string)

    def test_add_spaces_add_space_if_space_at_the_begin(self) -> None:
        words = self.elements[2].split()
        add_spaces(self.elements[2], words)
        modify_string = " ".join(words)

        self.assertEqual(self.elements[2].string, modify_string)

    def test_add_spaces_add_space_if_space_at_the_begin_and_end(self) -> None:
        words = self.elements[3].split()
        add_spaces(self.elements[3], words)
        modify_string = " ".join(words)

        self.assertEqual(self.elements[3].string, modify_string)
