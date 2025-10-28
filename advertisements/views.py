from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Advertisement
from .serializers import AdvertisementSerializer

# List all adverts
@api_view(['GET'])
def adverts_list(request):
    adverts = Advertisement.objects.filter(is_active=True).order_by('-date')
    serializer = AdvertisementSerializer(adverts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])      # لا تستخدم SessionAuth → تجنب CSRF
@permission_classes([AllowAny])  # يمكن تغييره لاحقًا للأمان
def advert_create(request):

    data = request.data.copy()  # انسخ البيانات لأنه يمكن تعديلها
    if 'image' in request.FILES:
        data['image_url'] = request.FILES['image_url']  # CloudinaryField يستخدم request.FILES

    serializer = AdvertisementSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Advertisement created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# Retrieve or update or delete one advert
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([])      # disable session auth for write ops (adjust per security)
@permission_classes([AllowAny])
def advert_detail(request, advert_id):
    try:
        advert = Advertisement.objects.get(id=advert_id)
    except Advertisement.DoesNotExist:
        return Response({"detail": "Advertisement not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdvertisementSerializer(advert)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = AdvertisementSerializer(advert, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Advertisement updated", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    advert.delete()
    return Response({"message": "Advertisement deleted"}, status=status.HTTP_200_OK)
