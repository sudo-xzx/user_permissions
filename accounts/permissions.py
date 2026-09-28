from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


def is_in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or is_in_group(user, "admin"))


def is_moderator(user):
    return user.is_authenticated and (is_admin(user) or is_in_group(user, "moderator"))


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = ()
    raise_exception = True

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=self.group_required).exists()

    def handle_no_permission(self):
        raise PermissionDenied("Недостаточно прав для доступа к этой странице.")
