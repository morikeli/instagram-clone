from django.shortcuts import redirect
from django.db.models import Q
from .models import Message
from accounts.models import User


def send_new_message(request):
    selected_user = request.POST.get('selected-follower')

    if selected_user:
        to_user = User.objects.get(username=selected_user)
        Message.send_message(from_user=request.user, to_user=to_user, msg='')
        
        return redirect('inbox')

    return redirect('inbox')
