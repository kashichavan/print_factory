from decimal import Decimal
from django.db import models
from apps.core.models import PublishableModel

class Service(PublishableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    badge = models.CharField(max_length=80, blank=True, default="01 / SERVICE")
    summary = models.CharField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    tags_csv = models.CharField(max_length=500, blank=True, help_text="Comma-separated spec tags")
    speed_info = models.CharField(max_length=100, blank=True, default="Standard 2-3 Days")
    base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("490.00"))
    image = models.ImageField(upload_to="content/services/", blank=True, null=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "title"]

    def __str__(self):
        return self.title

    @property
    def get_image_url(self):
        if self.image:
            url_str = str(self.image)
            if url_str.startswith("http://") or url_str.startswith("https://") or url_str.startswith("/"):
                return url_str
            elif url_str.startswith("images/"):
                return f"/static/{url_str}"
            try:
                return self.image.url
            except Exception:
                return f"/static/{url_str}"
        if "digital" in self.slug:
            return "/static/images/digital-printing.png"
        elif "offset" in self.slug:
            return "/static/images/offset-printing.png"
        elif "display" in self.slug or "signage" in self.slug:
            return "/static/images/display-solutions.png"
        elif "gifting" in self.slug or "merch" in self.slug:
            return "/static/images/corporate-gifting.png"
        return "/static/images/digital-printing.png"

    @property
    def tags_list(self):
        if not self.tags_csv:
            return []
        return [t.strip() for t in self.tags_csv.split(",") if t.strip()]


class PartnerLogo(PublishableModel):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="content/partners/")
    website_url = models.URLField(blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "name"]


class FAQ(PublishableModel):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position"]
