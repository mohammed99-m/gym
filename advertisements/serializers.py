from rest_framework import serializers
from .models import Advertisement

from rest_framework import serializers
from .models import Advertisement
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'content', 'image_url', 'date', 'is_active']
        read_only_fields = ['id', 'date']

    def create(self, validated_data):
        # Pop file if present to avoid Cloudinary upload during model.save()
        file_obj = validated_data.pop('image_url', None)

        # Create instance without the file
        instance = Advertisement.objects.create(**validated_data)

        if file_obj:
            try:
                # Try uploading manually and assign result to CloudinaryField
                result = cloudinary.uploader.upload(file_obj)
                # result['public_id'] or result['secure_url'] depending on how you want to store
                # CloudinaryField expects a public_id / resource string — simply assign the secure_url
                # If your CloudinaryField stores a public id, use result['public_id'].
                instance.image_url = result.get('public_id') or result.get('secure_url')
                instance.save(update_fields=['image_url'])
            except Exception:
                logger.exception("Cloudinary upload failed, returning created advert without image")
                # keep instance without image, don't raise to avoid 500
        return instance