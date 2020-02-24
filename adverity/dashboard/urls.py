from django.urls import path

from adverity.dashboard.views import (
        IndexView
)

app_name = "dashboard"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
]
