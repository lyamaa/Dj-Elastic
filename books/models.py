import json

from django.conf import settings
from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

# States indicate the publishing status of the book. Publishing might
# be in-progress, not yet published, published, rejected, etc.
BOOK_PUBLISHING_STATUS_PUBLISHED = "published"
BOOK_PUBLISHING_STATUS_NOT_PUBLISHED = "not_published"
BOOK_PUBLISHING_STATUS_IN_PROGRESS = "in_progress"
BOOK_PUBLISHING_STATUS_CANCELLED = "cancelled"
BOOK_PUBLISHING_STATUS_REJECTED = "rejected"
BOOK_PUBLISHING_STATUS_CHOICES = (
    (BOOK_PUBLISHING_STATUS_PUBLISHED, "Published"),
    (BOOK_PUBLISHING_STATUS_NOT_PUBLISHED, "Not published"),
    (BOOK_PUBLISHING_STATUS_IN_PROGRESS, "In progress"),
    (BOOK_PUBLISHING_STATUS_CANCELLED, "Cancelled"),
    (BOOK_PUBLISHING_STATUS_REJECTED, "Rejected"),
)
BOOK_PUBLISHING_STATUS_DEFAULT = BOOK_PUBLISHING_STATUS_PUBLISHED


class Publisher(models.Model):

    name = models.CharField(_("Publisher Name"), max_length=255)
    address = models.CharField(_("Publisher Address"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    state_province = models.CharField(_("State"), max_length=255)
    country = models.CharField(_("Country"), max_length=255)
    website = models.URLField(_("Publisher Website URL"))
    latitiude = models.DecimalField(_("Latitude"), null=True, blank=True, decimal_places=15, max_digits=19, default=0)
    longitude = models.DecimalField(_("Longitude"), null=True, blank=True, decimal_places=15, max_digits=19, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name

    @property
    def loaction_field_indexing(self):

        return {"lat": self.latitiude, "lon": self.longitude}


class Author(models.Model):
    """Author model"""

    salutation = models.CharField(_("Salutation"), max_length=255)
    name = models.CharField(_("Author Name"), max_length=255)
    email = models.EmailField(_("Author Email"), max_length=255)
    avatar = models.ImageField(_("Author Image"), upload_to="author", null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    "TAG MODEL"
    title = models.CharField(_("Title"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(_("Book Title"), max_length=255)
    description = models.TextField(_("Book Description"), null=True, blank=True)
    summary = models.TextField(_("Book Summary"), null=True, blank=True)
    authors = models.ManyToManyField("Author", verbose_name=_("Authors"), related_name="books")
    publisher = models.ForeignKey(Publisher, related_name="books", on_delete=models.RESTRICT)
    publication_date = models.DateField(_("Publication Date"), auto_now=False, auto_now_add=False)
    state = models.CharField(
        _("State"), max_length=255, choices=BOOK_PUBLISHING_STATUS_CHOICES, default=BOOK_PUBLISHING_STATUS_DEFAULT
    )
    isbn = models.CharField(_("ISBN"), max_length=255, unique=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(_("Pages No"), default=200)
    stock_count = models.PositiveIntegerField(_("Stock Count"), default=30)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tag"), related_name="books", blank=True)

    class Meta:
        ordering = ["isbn"]

    def _str__(self):
        return self.title

    @property
    def publisher_indexing(self):
        """Publisher for indexing.

        Used in Elasticsearch indexing.
        """
        if self.publisher is not None:
            return self.publisher.name

    @property
    def tags_indexing(self):
        return [tag.title for tag in self.tags.all()]
