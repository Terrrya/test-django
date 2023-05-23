from django.test import TestCase

from proxy.views import check_word


class CheckWordTests(TestCase):
    def test_check_word_return_true_if_word_have_6_letters(self) -> None:
        word = "123456"
        self.assertTrue(check_word(word))

    def test_check_word_return_false_if_word_have_gt_6_letters(self) -> None:
        word = "12345678"
        self.assertFalse(check_word(word))

    def test_check_word_return_false_if_word_have_lt_6_letters(self) -> None:
        word = "1234"
        self.assertFalse(check_word(word))

    def test_check_word_return_false_if_word_ends_on_punctuation(self) -> None:
        word = "12345,"
        self.assertFalse(check_word(word))
