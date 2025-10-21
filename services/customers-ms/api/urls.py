from django.contrib import admin
from django.urls import path
from api.views import CustomerCreateListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("customers/", CustomerCreateListView.as_view()),
]
