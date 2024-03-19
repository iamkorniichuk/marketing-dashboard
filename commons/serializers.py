from rest_framework import serializers


class RepresentativePkRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, serializer_class, **kwargs):
        self.serializer_class = serializer_class
        super().__init__(**kwargs)

    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)

        pk = value.pk
        queryset = self.get_queryset().filter(pk=pk)
        if queryset.exists():
            return self.serializer_class(queryset.first()).data
