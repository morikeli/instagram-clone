from ..models import Notification


def notifications(request):
    notification_qs = Notification.objects.filter(receiver=request.user)
    total_notifications = notification_qs.count()

    context = {'notifications': notification_qs, 'total_notifications': total_notifications}
    return context