from accounts.models import Notification

class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            notification_count = Notification.objects.filter(user=user, is_read=False).count()
            request.notification_count = notification_count
        else:
            request.notification_count = 0

        response = self.get_response(request)

        return response
