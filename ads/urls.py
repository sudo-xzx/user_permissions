from django.urls import path

from . import views

app_name = "ads"

urlpatterns = [
    path("", views.AdListView.as_view(), name="list"),
    path("ads/<int:pk>/", views.AdDetailView.as_view(), name="detail"),
    path("ads/create/", views.AdCreateView.as_view(), name="create"),
    path("ads/<int:pk>/edit/", views.AdUpdateView.as_view(), name="update"),
    path("ads/<int:pk>/delete/", views.AdDeleteView.as_view(), name="delete"),
]
