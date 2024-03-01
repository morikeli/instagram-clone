from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from accounts.models import User
from users.models import Friend
from .models import Message



@method_decorator(login_required(login_url='login'), name='get')
class InboxMessagesView(View):
    template_name = 'core/inbox.html'


    def get(self, request, *args, **kwargs):
        followers_qs = Friend.objects.filter(Q(following=request.user) | Q(follower=request.user))
        inbox_messages = Message.get_inbox_messages(user=request.user)
        active_user = None  # currently logged in user(s)
        directs = None

        if inbox_messages:
            _message = inbox_messages[0]
            active_user = _message["user"].username
            directs = Message.objects.filter(receiver=_message["user"], is_read=True)
            # directs.update(is_read=True)
            

            for msg in inbox_messages:
                if msg["user"].username == active_user:
                    msg["unread"] = 0
        
        context = {
            'direct_messages': directs,
            'inbox_messages': inbox_messages,
            'active_user': active_user,
            'followers': followers_qs,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
class DirectMessagesView(View):
    template_name = 'core/inbox.html'


    def get(self, request, dm_user, *args, **kwargs):
        user_msgs = Message.get_inbox_messages(user=request.user)
        active_user = dm_user
        directs = Message.objects.filter(receiver__username=dm_user)
        directs.update(is_read=True)

        
        for msg in user_msgs:
            if msg["user"].username == dm_user:
                msg["unread"] = 0

        context = {
            'direct_messages': directs,
            'inbox_messages': user_msgs,
            'active_user': active_user,
        }
        return render(request, self.template_name, context)
    

    def post(self, request, dm_user, *args, **kwargs):
        msg_receiver = request.POST.get('to-user')
        message_txt = request.POST.get('text-message')


        if message_txt and msg_receiver:
            get_user = User.objects.get(username=msg_receiver)
            get_empty_msgs = Message.objects.filter(sender=request.user, text='').delete()
            save_msg = Message.send_message(from_user=request.user, to_user=get_user, msg=message_txt)
        
        return redirect('direct_message', dm_user)
