from django.db.models import Q, QuerySet


class TodoQuerySet(QuerySet):
    def contains_text(self, text: str):
        return self.filter(
            Q(title__icontains=text) | Q(text__icontains=text)
        )
