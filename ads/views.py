from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Ad


class AdListView(ListView):
    model = Ad
    template_name = "ads/ad_list.html"
    context_object_name = "ads"
    paginate_by = 20

    def get_queryset(self):
        return Ad.objects.select_related("author")


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Ad
    fields = ("title", "description")
    template_name = "ads/ad_form.html"
    permission_required = "ads.add_ad"
    success_url = reverse_lazy("ads:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ("title", "description")
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:list")
    raise_exception = True

    def test_func(self):
        ad = self.get_object()
        user = self.request.user
        is_owner_with_perm = ad.author_id == user.id and user.has_perm("ads.change_ad")
        can_edit_any = user.has_perm("ads.can_edit_any_ad")
        return is_owner_with_perm or can_edit_any


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = "ads/ad_confirm_delete.html"
    success_url = reverse_lazy("ads:list")
    raise_exception = True

    def test_func(self):
        ad = self.get_object()
        user = self.request.user
        is_owner_with_perm = ad.author_id == user.id and user.has_perm("ads.delete_ad")
        can_delete_any = user.has_perm("ads.can_delete_any_ad")
        return is_owner_with_perm or can_delete_any
