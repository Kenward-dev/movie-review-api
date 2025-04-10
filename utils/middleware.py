from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404


class AdminAccessMiddleware:
    """
    Middleware to restrict Django admin access to superusers only.
    Allows access to login, logout, and password reset views for all users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index').split('index')[0]):
            try:
                match = resolve(request.path)
                view_name = match.view_name
            except Resolver404:
                view_name = None

            whitelisted_views = {
                'admin:login',
                # 'admin:logout',
                # 'admin:password_reset',
                # 'admin:password_reset_done',
                # 'admin:password_reset_confirm',
                # 'admin:password_reset_complete',
            }

            if view_name in whitelisted_views:
                return self.get_response(request)

            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('admin:login'))

            if not request.user.is_superuser:
                return HttpResponseForbidden("Access denied. Superuser privileges required.")

        return self.get_response(request)
