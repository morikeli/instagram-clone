from ..models import Notification


def notifications(request):
    total_notifications = Notification.objects.filter(receiver=request.user, is_read=False).count()

    context = {'total_notifications': total_notifications}
    return context