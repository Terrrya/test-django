from django.urls import re_path

from proxy.views import hacker_news_proxy

app_name = "proxy"

urlpatterns = [re_path(r"^", hacker_news_proxy, name="hacker-news-proxy")]
