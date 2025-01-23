from django.urls import path
from . import views
from .views import ItemAPIView, CreateItemAPIView

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_get, name="create_get"),
    path("details/<item_id>/<type>", views.details, name="details"),
    path('api/item/<type>', ItemAPIView.as_view(), name='story-list'),
    path('delete_item/<itemId>/<type>', views.delete_item, name='delete_item'),
    path('modify_item/<itemId>/<type>', views.modify_item, name='modify_item'),
    path('get_item/<itemId>/<type>', views.get_item, name='get_item'),
    path('api/item/create/<type>', CreateItemAPIView.as_view(), name='create-item'),
    

]