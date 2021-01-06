from django.core.files.base import ContentFile

from base64 import b64decode

from rest_framework import serializers


class StdImageField(serializers.ImageField):
    def to_representation(self, obj):
        return_object = {}
        field = obj.field
        if hasattr(field, 'variations'):
            variations = field.variations
            for key, attr in variations.items():
                if hasattr(obj, key):
                    field_obj = getattr(obj, key, None)
                    url = None
                    if field_obj:
                        url = getattr(field_obj, 'url', None)
                    if url:
                        request = self.context.get('request', None)
                        if request is not None:
                            url = request.build_absolute_uri(url)
                        return_object[key] = url
        return return_object

    def to_internal_value(self, data):
        if not data:
            return

        if isinstance(data, str) and data.startswith('data:image'):
            img_format, img_str = data.split(';base64,')
            ext = img_format.split('/')[-1]
            data = ContentFile(b64decode(img_str), name='temp.' + ext)
        return super(StdImageField, self).to_internal_value(data)
