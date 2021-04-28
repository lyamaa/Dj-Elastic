from django.contrib import admin

from .models import Author, Book, Publisher, Tag


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book Admin"""

    list_display = ("title", "isbn", "price", "publication_date")
    search_fields = ("title",)
    filter_horizontal = ("authors", "tags")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author Admin"""

    list_display = ("name", "email")
    search_fields = ("name",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag Admin"""

    list_display = ("title",)
    search_fields = ("title",)
