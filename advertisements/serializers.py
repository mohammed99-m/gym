# serializers.py
from rest_framework import serializers
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    # write-only field to accept uploaded file
    image = serializers.ImageField(write_only=True, required=False)
    # read-only field to expose uploaded image URL
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'content', 'image', 'image_url', 'date', 'is_active']
        read_only_fields = ['id', 'date', 'image_url']

    def get_image_url(self, obj):
        if not obj.image_url:
            return None
        try:
            return obj.image_url.url
        except Exception:
            return str(obj.image_url)

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        advert = Advertisement.objects.create(**validated_data)
        if image:
            advert.image_url = image
            advert.save()
        return advert

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if image:
            instance.image_url = image
        instance.save()
        return instance