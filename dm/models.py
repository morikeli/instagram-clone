from django.db import models
from accounts.models import User


class Message(models.Model):
    id = models.CharField(max_length=25, primary_key=True, unique=True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', editable=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', editable=False)
    text = models.TextField(null=True, blank=False)
    is_read = models.BooleanField(default=False, editable=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['date_sent']
    

    def send_message(from_user, to_user, msg):
        """ This function is used to send and save messages and replies. """
        # sender's message
        sender_message = Message.objects.create(
            sender=from_user,
            receiver=to_user,
            text=msg,
            is_read=True,
        )
        sender_message.save()

        return sender_message
    

    def get_inbox_messages(user):
        """ This functions is used to get messages sent to the currently logged in user's inbox """
        users_lists = []
        msgs = Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).values('receiver').annotate(last_msg=models.Max('date_sent')).order_by('-last_msg')

        for message in msgs:
            users_lists.append({
                'user': User.objects.get(pk=message["receiver"]),
                'last': message["last_msg"],
                "unread": Message.objects.filter(sender=user, receiver__pk=message["receiver"], is_read=False).count(),
                'last_message': [last_text.text for last_text in Message.objects.filter(receiver__pk=message["receiver"]).order_by('-date_sent')][0]    # get the last sent message in user's chat
            })
        
        return users_lists