from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics




class AdvertisementListApi(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    

# List all adverts
@api_view(['GET'])
def adverts_list(request):
    adverts = Advertisement.objects.filter(is_active=True).order_by('-date')
    serializer = AdvertisementSerializer(adverts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework import generics, permissions

class AdvertisementListCreateAPIView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all().order_by('-date')
    serializer_class = AdvertisementSerializer
    parser_classes = [MultiPartParser, FormParser]  # مهم لرفع الصور

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



from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import cloudinary.uploader
import traceback

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def advert_create_debug(request):
    # Show what we received
    files_keys = list(request.FILES.keys())
    files_info = {k: {'name': v.name, 'size': getattr(v, 'size', None)} for k, v in request.FILES.items()}
    data_keys = list(request.data.keys())

    upload_result = None
    upload_exc = None

    # If file arrived, try to upload to Cloudinary (only for debug)
    if 'image_url' in request.FILES:
        try:
            result = cloudinary.uploader.upload(request.FILES['image_url'])
            upload_result = {
                'public_id': result.get('public_id'),
                'secure_url': result.get('secure_url'),
                'raw': {k: result.get(k) for k in ('bytes', 'format', 'width', 'height') if k in result}
            }
        except Exception as e:
            upload_exc = traceback.format_exc()

    return Response({
        "FILES_keys": files_keys,
        "FILES_info": files_info,
        "DATA_keys": data_keys,
        "cloudinary_upload_result": upload_result,
        "cloudinary_exception": upload_exc
    })
