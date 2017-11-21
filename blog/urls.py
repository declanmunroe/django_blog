from django.conf.urls import url
from .views import show_posts, view_post, add_post, edit_post, add_comment


urlpatterns = [
    url(r"^posts$", show_posts, name = "show_posts"),
    url(r"^view_post/(\d+)", view_post, name = "view_post"),
    url(r"^add_post", add_post, name = "add_post"),
    url(r"^edit_post/(\d+)", edit_post, name = "edit_post"),
    url(r"^add_comment/(\d+)", add_comment, name="add_comment"),
    ]