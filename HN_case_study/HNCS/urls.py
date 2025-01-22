from django.urls import path
from . import views
from .views import ItemAPIView

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<item_id>", views.details, name="details"),
    path('api/item/<type>', ItemAPIView.as_view(), name='story-list'),

]