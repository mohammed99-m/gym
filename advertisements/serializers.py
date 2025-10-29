from rest_framework import serializers
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    # allow client to POST image_public_id when they uploaded directly to Cloudinary
    image_public_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'content', 'image_url', 'date', 'is_active', 'image_public_id']
        read_only_fields = ['id', 'date']

    def create(self, validated_data):
        public_id = validated_data.pop('image_public_id', None)
        # If validated_data contains a file (CloudinaryField will be handled by model save),
        # create the instance and then attach public_id if provided
        instance = Advertisement.objects.create(**validated_data)

        if public_id:
            # CloudinaryField expects a public_id string
            instance.image_url = public_id
            instance.save(update_fields=['image_url'])
        return instance