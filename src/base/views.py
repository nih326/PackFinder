#
# Created on Sun Nov 04 2024
#
# The MIT License (MIT)
# Copyright (c) 2024 Chaitralee Datar, Ananya Patankar, Yash Shah
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

from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SignUpForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .filters import ProfileFilter
from .matching import matchings, calculate_preference_match

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from base.tokens import account_activation_token
from django.views import View
from .models import Room
from .forms import RoomForm


class ActivateAccount(View):
    """Account activation"""

    def get(self, request, uidb64, token, *args, **kwargs):
        """GET method for the Account activation."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(
            user, token
        ):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(
                request,
                ("Your account has been confirmed. We have logged you in."),
            )
            return redirect("home")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("home")


class SignUpView(generic.CreateView):
    """Sign up View"""

    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        current_site = get_current_site(self.request)
        subject = "Activate Your FindMyRoomie Account"
        message = render_to_string(
            "emails/account_activation_email.html",
            {
                "user": self.object,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(self.object.pk)),
                "token": account_activation_token.make_token(self.object),
            },
        )
        self.object.email_user(subject, message)

        messages.success(
            self.request,
            ("Please Confirm your email to complete registration."),
        )

        return HttpResponseRedirect(self.get_success_url())


def home(request):
    """Render Home Page"""
    user_count = get_user_model().objects.all().count()
    return render(request, "index.html", {"user_count": user_count})


@login_required()
def profile(request):
    """Render Profile page"""
    return render(request, "pages/profile.html", {"profile": request.user.profile})


@login_required()
def profile_edit(request):
    """Render Edit Profile Page"""
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.is_profile_complete = True
            print(p.profile_photo)
            p.save()

            return redirect("profile")

    person = Profile.objects.all()
    form = ProfileForm(instance=profile)
    return render(
        request, "pages/profile_edit.html", {"form": form, "profiles": person}
    )


@login_required()
def findpeople(request):
    """Render findpeople page"""
    user_profile = request.user.profile
    profiles = Profile.objects.exclude(user=request.user)
    
    # Calculate match percentages
    profiles_with_match = []
    for profile in profiles:
        match_percentage = calculate_preference_match(user_profile, profile)
        profiles_with_match.append({
            'profile': profile,
            'match_percentage': round(match_percentage, 1)
        })
    
    # Sort by match percentage
    profiles_with_match.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    context = {
        'profiles': profiles_with_match
    }
    return render(request, 'pages/findpeople.html', context)


@login_required
def myroom(request):
    """Handle My Room functionality"""
    profile = request.user.profile
    
    # Get rooms where the user has shown interest
    interested_rooms = Room.objects.filter(interested_users=profile)
    
    # Get rooms owned by the user
    owned_rooms = Room.objects.filter(owner=profile)
    
    context = {
        'interested_rooms': interested_rooms,
        'owned_rooms': owned_rooms,
        'profile': profile
    }
    
    return render(request, "pages/myroom.html", context)


@login_required
def add_room(request):
    """Add a new room listing"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user.profile
            room.save()
            return redirect('myroom')
    else:
        form = RoomForm()
    
    return render(request, 'pages/add_room.html', {'form': form})


def user_logout(request):
    """Log out and redirect to Home Page"""
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")


@login_required
def toggle_room_interest(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        profile = request.user.profile
        
        if profile in room.interested_users.all():
            room.interested_users.remove(profile)
            messages.success(request, "Removed interest in room.")
        else:
            room.interested_users.add(profile)
            messages.success(request, "Added interest in room.")
            
        return redirect('myroom')
    except Room.DoesNotExist:
        messages.error(request, "Room not found.")
        return redirect('myroom')

#
# Created on Sun Oct 09 2022
#
# The MIT License (MIT)
# Copyright (c) 2022 Rohit Geddam, Arun Kumar, Teja Varma, Kiron Jayesh, Shandler Mason
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

from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, SignUpForm
from .models import Profile
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .filters import ProfileFilter
from .matching import matchings

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from base.tokens import account_activation_token
from django.views import View


class ActivateAccount(View):
    """Account activation"""

    def get(self, request, uidb64, token, *args, **kwargs):
        """GET method for the Account activation."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(
            user, token
        ):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(
                request,
                ("Your account has been confirmed. We have logged you in."),
            )
            return redirect("home")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("home")


class SignUpView(generic.CreateView):
    """Sign up View"""

    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        current_site = get_current_site(self.request)
        subject = "Activate Your FindMyRoomie Account"
        message = render_to_string(
            "emails/account_activation_email.html",
            {
                "user": self.object,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(self.object.pk)),
                "token": account_activation_token.make_token(self.object),
            },
        )
        self.object.email_user(subject, message)

        messages.success(
            self.request,
            ("Please Confirm your email to complete registration."),
        )

        return HttpResponseRedirect(self.get_success_url())


def home(request):
    """Render Home Page"""
    user_count = get_user_model().objects.all().count()
    return render(request, "index.html", {"user_count": user_count})


@login_required()
def profile(request):
    """Render profile page"""
    if not request.user.profile.is_profile_complete:
        messages.error(request, "Please complete your profile first!")
        return redirect("profile_edit")

    profile = Profile.objects.get(user=request.user)

    return render(request, "pages/profile.html", {"profile": profile})


@login_required()
def profile_edit(request):
    """Render Edit Profile Page"""
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.is_profile_complete = True
            print(p.profile_photo)
            p.save()

            return redirect("profile")

    person = Profile.objects.all()
    form = ProfileForm(instance=profile)
    return render(
        request, "pages/profile_edit.html", {"form": form, "profiles": person}
    )


@login_required()
def findpeople(request):
    """Render findpeople page"""
    qs = Profile.objects.filter(visibility=True).exclude(user=request.user)
    f = ProfileFilter(request.GET, queryset=qs)
    return render(request, "pages/findpeople.html", {"filter": f})


@login_required()
def myroom(request):
    """Render Myroom page based on Profile Completion"""
    if not request.user.profile.is_profile_complete:
        messages.error(request, "Please complete your profile first!")
        return redirect("profile_edit")

    matches = matchings(request.user)

    return render(request, "pages/myroom.html", {"matches": matches})


def user_logout(request):
    """Log out and redirect to Home Page"""
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

User = get_user_model()

@login_required
def chat_list(request):
    """Show list of all chats for current user"""
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chat/chat_list.html', {'chat_rooms': chat_rooms})

@login_required
def chat_room(request, room_id):
    """Show individual chat room and its messages"""
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Check if user is participant
    if request.user not in room.participants.all():
        return redirect('chat_list')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
    
    messages = room.messages.all()
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages
    })

@login_required
def create_chat_room(request, user_id):
    """Create a new chat room with another user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Check if chat room already exists
    existing_room = ChatRoom.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_room:
        return redirect('chat_room', room_id=existing_room.id)
    
    # Create new room
    room = ChatRoom.objects.create()
    room.participants.add(request.user, other_user)
    
    return redirect('chat_room', room_id=room.id)



@login_required
def clear_chat(request, room_id):
    """Clear all messages in a chat room"""
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, id=room_id)
        
        # Verify user is a participant
        if request.user not in room.participants.all():
            messages.error(request, "You don't have permission to clear this chat.")
            return redirect('chat_list')
        
        try:
            # Delete all messages except system welcome messages
            room.messages.exclude(sender=None).delete()
            
            # Add system message about clearing
            Message.objects.create(
                room=room,
                sender=None,  # System message
                content="🧹 Chat history has been cleared."
            )
            
            messages.success(request, "Chat history cleared successfully.")
        except Exception as e:
            print(f"Error clearing chat: {e}")  # Debug print
            messages.error(request, "An error occurred while clearing the chat.")
        
    return redirect('chat_room', room_id=room_id)

    from django.shortcuts import render

def forum_home(request):
    return render(request, 'forum/forum_home.html')

def housing_tips(request):
    return render(request, 'forum/housing_tips.html')

def roommate_issues(request):
    return render(request, 'forum/roommate_issues.html')

def campus_life(request):
    return render(request, 'forum/campus_life.html')