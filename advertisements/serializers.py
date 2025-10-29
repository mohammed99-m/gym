# serializers.py
from rest_framework import serializers
from .models import Advertisement
from cloudinary.utils import cloudinary_url

class AdvertisementSerializer(serializers.ModelSerializer):
    image_public_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    image_url_full = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id','title','content','image_url','image_url_full','date','is_active','image_public_id']
        read_only_fields = ['id','date']

    def get_image_url_full(self, obj):
        try:
            public_id = obj.image_url
            if not public_id:
                return None
            url, _ = cloudinary_url(public_id, secure=True)
            return url
        except Exception:
            return None

    def create(self, validated_data):
        public_id = validated_data.pop('image_public_id', None)
        instance = Advertisement.objects.create(**validated_data)
        if public_id:
            instance.image_url = public_id
            instance.save(update_fields=['image_url'])
        return instance
