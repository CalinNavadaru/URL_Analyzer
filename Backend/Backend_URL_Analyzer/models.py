from django.db import models

class URLCheck(models.Model):
    url = models.URLField()
    verdict = models.CharField(max_length=20)
    checked_at = models.DateTimeField(auto_now_add=True)
    user_feedback = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.url} - {self.verdict}"