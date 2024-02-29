from django.urls import path
from . import views
from . import htmx


urlpatterns = [
    path('inbox/', views.InboxMessagesView.as_view(), name='inbox'),
    path('<str:dm_user>/', views.DirectMessagesView.as_view(), name='direct_message'),
]


htmx_urlpatterns = [
    path('', htmx.send_new_message, name='text_searched_follower'),
]


urlpatterns += htmx_urlpatterns