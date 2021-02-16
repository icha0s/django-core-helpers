from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.utils import timezone


class DeletableQuerySetMixin:
    """Custom `Deletable` QuerySet Mixin for DeletableModel."""

    def delete(self, force: bool = False):
        """Delete the objects from current QuerySet (sets its ``is_deleted`` field to True). """
        if force:
            """Hard delete the objects if `force` param is True"""
            return super().delete()
        else:
            return self.count(), self.update(is_deleted=True, deleted_at=timezone.now())  # noqa


class DeletableQuerySet(DeletableQuerySetMixin, QuerySet):
    """Custom `Deletable` QuerySet for `DeletableManager`."""


class DeletableManagerMixin:

    _queryset_class = DeletableQuerySet

    def get_queryset(self):
        """Returns custom queryset with filter `is_deleted=False`."""

        kwargs = {"model": self.model, "using": self._db}
        if hasattr(self, "_hints"):
            kwargs["hints"] = self._hints

        return self._queryset_class(**kwargs).filter(is_deleted=False)


class GetOrNoneManagerMixin:
    def get_or_none(self, **kwargs):
        """Return model instance or None by `**kwargs`."""
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class ActiveManagerMixin:
    def get_queryset(self):
        """Return custom queryset with filter `is_active=True`."""
        return super().get_queryset().filter(is_active=True)


class DeletableManager(DeletableManagerMixin, GetOrNoneManagerMixin, Manager):
    """Custom manager that returns records with an `is_deleted` flag set as `False`."""


class ActiveManager(ActiveManagerMixin, GetOrNoneManagerMixin, Manager):
    """Custom manager  that Return records with an `is_active` flag set as `True`."""


class ActiveDeletableManager(DeletableManagerMixin, ActiveManagerMixin, GetOrNoneManagerMixin, Manager):
    """Custom manager  records with an `is_active` flag set as `True` and `is_deleted` flag as `False`."""
