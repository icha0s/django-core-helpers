import uuid

from django.core.exceptions import ValidationError
from django.db.models import BooleanField, DateTimeField
from django.db.models import UUIDField as _UUIDField
from django.utils.translation import gettext_lazy as _


class AutoCreatedField(DateTimeField):
    """
    AutoCreatedField

    By default, sets auto_now_add=True
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_now_add", True)
        super().__init__(self, *args, **kwargs)


class AutoModifiedField(DateTimeField):
    """
    AutoModifiedField

    By default, auto_now=True
    Sets value to now every time the object is saved.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_now", True)
        super().__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        if not getattr(model_instance, "update_modified", True):
            return getattr(model_instance, self.attname)
        return super().pre_save(model_instance, add)


class UUIDFieldMixin:
    """UUIDFieldMixin sets the default value."""

    DEFAULT_MAX_LENGTH = 36

    def __init__(self, verbose_name=None, primary_key=True, version=4, editable=False, *args, **kwargs):
        kwargs.setdefault("max_length", self.DEFAULT_MAX_LENGTH)
        kwargs.setdefault("primary_key", primary_key)
        kwargs.setdefault("editable", editable)
        kwargs.setdefault("default", self._get_default(version))
        super().__init__(verbose_name, *args, **kwargs)

    @classmethod
    def _get_default(cls, version):

        if version == 2:
            raise ValidationError(_("UUID version 2 is not supported."))

        if version < 1 or version > 5:
            raise ValidationError(_("UUID version is not valid."))

        if version == 1:
            return uuid.uuid1
        elif version == 3:
            return uuid.uuid3
        elif version == 4:
            return uuid.uuid4
        elif version == 5:
            return uuid.uuid5


class UUIDField(UUIDFieldMixin, _UUIDField):
    """UUID field to use as primary key of model.

    By default, sets primary_key=True, version=4, editable=False
    """


class AutoActiveField(BooleanField):
    """
    AutoActiveField

    By default, sets default=True
    """

    def __init__(self, verbose_name=_("Is active?"), default=True, *args, **kwargs):
        kwargs.setdefault("default", default)
        super().__init__(self, verbose_name, *args, **kwargs)
