from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class UuidModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    id = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = self.__class__.objects.all().aggregate(largest=models.Max("id"))["largest"]

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.id = last_id + 1

        super(UuidModel, self).save(*args, **kwargs)
