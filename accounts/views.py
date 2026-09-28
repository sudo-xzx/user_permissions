from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CustomUserCreationForm, ProfileForm
from .models import CustomUser, Profile
from .permissions import GroupRequiredMixin, is_admin


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:profile_edit")

    def form_valid(self, form):
        response = super().form_valid(form)
        user_group, _ = Group.objects.get_or_create(name="user")
        self.object.groups.add(user_group)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация прошла успешно. Заполните профиль.")
        return response


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно сохранён.")
            return redirect("ads:list")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile_edit.html", {"form": form})


class UserManagementListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = CustomUser
    template_name = "accounts/user_management_list.html"
    context_object_name = "users"
    group_required = ("admin",)
    paginate_by = 25

    def get_queryset(self):
        return CustomUser.objects.select_related("profile").prefetch_related("groups").all()


class UserManagementDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/user_management_detail.html"
    context_object_name = "target_user"
    group_required = ("admin",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_groups"] = Group.objects.all()
        return context


@login_required
def user_toggle_active(request, pk):
    if not is_admin(request.user):
        messages.error(request, "Недостаточно прав.")
        return redirect("accounts:user_management_list")
    target = get_object_or_404(CustomUser, pk=pk)
    target.is_active = not target.is_active
    target.save(update_fields=["is_active"])
    messages.success(request, f"Статус пользователя {target.email} обновлён.")
    return redirect("accounts:user_management_detail", pk=pk)


@login_required
def user_set_group(request, pk):
    if not is_admin(request.user):
        messages.error(request, "Недостаточно прав.")
        return redirect("accounts:user_management_list")
    target = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        group_name = request.POST.get("group")
        target.groups.clear()
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            target.groups.add(group)
        messages.success(request, f"Роль пользователя {target.email} обновлена.")
    return redirect("accounts:user_management_detail", pk=pk)


@login_required
def user_delete(request, pk):
    if not is_admin(request.user):
        messages.error(request, "Недостаточно прав.")
        return redirect("accounts:user_management_list")
    target = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        email = target.email
        target.delete()
        messages.success(request, f"Пользователь {email} удалён.")
        return redirect("accounts:user_management_list")
    return render(request, "accounts/user_confirm_delete.html", {"target_user": target})
