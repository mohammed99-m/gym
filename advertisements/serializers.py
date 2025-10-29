# serializers.py
from rest_framework import serializers
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    image_url_full = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'content', 'image_url', 'image_url_full', 'date', 'is_active']

    def get_image_url_full(self, obj):
        if obj.image_url:
            # CloudinaryField provides .url for the full URL
            return obj.image_url.url
        return None
