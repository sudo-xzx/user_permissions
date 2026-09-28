from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField("заголовок", max_length=200)
    description = models.TextField("описание", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="автор",
    )
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("обновлено", auto_now=True)

    class Meta:
        verbose_name = "объявление"
        verbose_name_plural = "объявления"
        ordering = ["-created_at"]
        permissions = [
            ("can_edit_any_ad", "Может редактировать любые объявления"),
            ("can_delete_any_ad", "Может удалять любые объявления"),
        ]

    def __str__(self):
        return self.title
