from rest_framework import serializers


class ObjectForTitleField(serializers.SlugRelatedField):
    """Переопределение метода to_representation
    для полей категория и жанры"""

    def to_representation(self, value):
        return {'name': value.name,
                'slug': value.slug}
