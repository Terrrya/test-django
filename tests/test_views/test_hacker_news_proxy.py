from unittest.mock import Mock, patch

from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from proxy.views import hacker_news_proxy


class HackerNewsProxyTests(TestCase):
    @patch("proxy.views.requests.get")
    def test_hacker_news_proxy_return_modify_html_page(
        self, mock_requests: Mock
    ) -> None:
        actual_page = (
            "<html>"
            "<head>"
            "</head>"
            "<body>"
            "<div>1234 123456 12345 1234567<div>"
            "</body>"
            "</html>"
        )
        mock_requests.return_value = HttpResponse(content=actual_page)

        response = hacker_news_proxy(HttpRequest())
        expected_page = (
            "<html>"
            "<head>"
            "</head>"
            "<body>"
            "<div>1234 123456™ 12345 1234567<div>"
            "</body>"
            "</html>"
        )

        mock_requests.assert_called_once_with("https://news.ycombinator.com")
        self.assertHTMLEqual(expected_page, response.content.decode("UTF-8"))
