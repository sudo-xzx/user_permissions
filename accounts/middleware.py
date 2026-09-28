from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and not user.is_superuser:
            path = request.path

            exempt_prefixes = (
                "/accounts/profile/",
                "/accounts/logout/",
                "/accounts/login/",
                "/accounts/register/",
                "/admin/",
                "/static/",
                "/media/",
            )

            if not any(path.startswith(p) for p in exempt_prefixes):
                profile = getattr(user, "profile", None)
                if profile is None or not profile.is_complete():
                    return redirect(reverse("accounts:profile_edit"))

        return self.get_response(request)