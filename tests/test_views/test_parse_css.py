from django.test import TestCase

from proxy.utils.parse_css import find_static_files_in_css


class ParseCSSTEsts(TestCase):
    def test_find_static_files_in_css_return_filenames(self):
        css_txt = """
            .votearrow {
                background-image: url("test.svg");
              }
            @media only screen {
                img[src='test.gif'][width='40'] { width: 12px; }
            }
        """

        expected_filenames = ["test.svg", "test.gif"]
        filenames = find_static_files_in_css(css_txt)

        self.assertIn("test.svg", filenames)
        self.assertIn("test.gif", filenames)
        self.assertEqual(2, len(filenames))
