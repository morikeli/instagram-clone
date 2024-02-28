from django.urls import path
from . import views


urlpatterns = [
    path('inbox/', views.InboxMessagesView.as_view(), name='inbox'),

]