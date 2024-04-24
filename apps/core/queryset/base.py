from django.db.models import Manager


class BaseManager(Manager):
    def filter(self, *args, **kwargs):
        queryset = super().filter(*args, **kwargs)
        return queryset.filter(deleted_at__isnull=True, is_active=True)
