#
# Created on Fri Nov 22 2024
#
# The MIT License (MIT)
# Copyright (c) 2024 Niharika Maruvanahalli Suresh , Diya Shetty, Sanjana Nanjangud Shreenivas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# accounts/urls.py
from django.urls import path
from .views import SignUpView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from base.views import ActivateAccount
from django.views.generic import TemplateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("findpeople/", views.findpeople, name="findpeople"),
    path("myroom/", views.my_room, name="my_room"),
    path("logout/", views.user_logout, name="user_logout"),
    path("chats/", views.chat_list, name="chat_list"),
    path("chat/<int:room_id>/", views.chat_room, name="chat_room"),
    path(
        "chat/create/<str:email>/",
        views.create_chat_room,
        name="create_chat_room",
    ),
    path("chat/<int:room_id>/clear/", views.clear_chat, name="clear_chat"),
    path('chat/create/', views.create_chat_redirect, name='create_chat_redirect'),
    path('roommate-agreement/<str:email>/', views.roommate_agreement, name='roommate_agreement'),
    path(
        "about",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccount.as_view(),
        name="activate",
    ),
    path("", views.home, name="home"),
    path("add-room/", views.add_room, name="add_room"),
    path(
        "toggle-interest/<int:room_id>/",
        views.toggle_room_interest,
        name="toggle_room_interest",
    ),
    path('forum/', views.forum_home, name='forum_home'),
    path('forum/housing-tips/', views.housing_tips, name='housing_tips'),
    path('forum/roommate-issues/', views.roommate_issues, name='roommate_issues'),
    path('forum/campus-life/', views.campus_life, name='campus_life')
    path(
        "remove_interest/<int:room_id>/",
        views.remove_interest,
        name="remove_interest",
    ),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
