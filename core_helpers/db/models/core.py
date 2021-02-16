from django.db.models import BooleanField, DateTimeField, Manager, Model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core_helpers.db.fields import (
    AutoActiveField,
    AutoCreatedField,
    AutoModifiedField,
    UUIDField,
)
from core_helpers.db.managers import (
    ActiveDeletableManager,
    ActiveManager,
    DeletableManager,
)


class UUIDModel(Model):
    """Abstract model with `uuid` id as primary key."""

    id = UUIDField(_("ID"))

    class Meta:
        abstract = True


class ActiveModel(Model):
    """Abstract `Active UUID` model."""

    is_active = AutoActiveField()

    objects = Manager()
    active = ActiveManager()

    class Meta:
        abstract = True


class TimeStampedModel(Model):
    """Abstract `Created` model."""

    created_at = AutoCreatedField(_("Created at"))
    modified_at = AutoModifiedField(_("Modified at"))

    def save(self, *args, **kwargs):
        self.update_modified = kwargs.pop("update_modified", getattr(self, "update_modified", True))
        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            kwargs["update_fields"] = set(update_fields).union({"modified_at"})

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class DeletableModel(Model):
    """Abstract `Deletable` model."""

    is_deleted = BooleanField(_("Is deleted"), default=False)
    deleted_at = DateTimeField(_("Deleted at"), null=True, blank=True, editable=False)

    objects = DeletableManager()
    all_objects = Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        """Delete the current instance."""
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save(using=using, update_fields=("is_deleted", "deleted_at"))


class DeletableUUIDModel(DeletableModel, UUIDModel):
    """Abstract `Deletable, UUID` mixin model."""

    class Meta:
        abstract = True


class ActiveUUIDModel(ActiveModel, UUIDModel):
    """Abstract `Active UUID` mixin model."""

    class Meta:
        abstract = True


class ActiveTimeStampedModel(ActiveModel, TimeStampedModel):
    """Abstract `Active TimeStamped` mixin model."""

    class Meta:
        abstract = True


class ActiveDeletableModel(ActiveModel, DeletableModel):
    """Abstract `Active Deletable` mixin model."""

    objects = DeletableManager()
    active = ActiveDeletableManager()
    all_objects = Manager()

    class Meta:
        abstract = True


class ActiveTimeStampedUUIDModel(ActiveModel, TimeStampedModel, UUIDModel):
    """Abstract `Active TimeStamped UUID` mixin model."""

    class Meta:
        abstract = True


class ActiveDeletableUUIDModel(ActiveDeletableModel, UUIDModel):
    """Abstract `Active Deletable` mixin model."""

    class Meta:
        abstract = True


class ActiveTimeStampedDeletableModel(TimeStampedModel, ActiveDeletableModel):
    """Abstract `Active, TimeStamped, Deletable` mixin model."""

    class Meta:
        abstract = True


class ActiveTimeStampedDeletableUUIDModel(TimeStampedModel, ActiveDeletableModel, UUIDModel):
    """Abstract `Active, TimeStamped, Deletable, UUID` mixin model."""

    class Meta:
        abstract = True


class TimeStampedDeletableModel(TimeStampedModel, DeletableModel):
    """Abstract `TimeStamped, Deletable` mixin model."""

    class Meta:
        abstract = True


class TimeStampedUUIDModel(TimeStampedModel, UUIDModel):
    """Abstract `TimeStamped, UUIDModel` mixin model."""

    class Meta:
        abstract = True


class TimeStampedDeletableUUIDModel(TimeStampedModel, DeletableModel, UUIDModel):
    """Abstract `TimeStamped, Deletable, UUID` mixin model."""

    class Meta:
        abstract = True
