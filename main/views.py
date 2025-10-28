from datetime import datetime, timedelta
from django.shortcuts import render
from .serializers import PlayerSerializer
from .models import Player
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Player
from .serializers import PlayerSerializer

@api_view(['POST'])
@authentication_classes([])        # No CSRF
@permission_classes([AllowAny])    # Allow all (for testing or Flutter client)
def login_player(request):
    phone = request.data.get('phone_number')
    password = request.data.get('password')

    # تحقق من إدخال البيانات
    if not phone or not password:
        return Response(
            {"error": "Phone number and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        player = Player.objects.get(phone_number=phone)
    except Player.DoesNotExist:
        return Response(
            {"error": "Invalid phone number or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # تحقق من صحة كلمة المرور
    if not check_password(password, player.password):
        return Response(
            {"error": "Invalid phone number or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # كل شيء تمام ✅
    now = datetime.now().date()
    if player.date:
            start_date = player.date
            # نحسب المدة المسموحة حسب النوع
            if player.type == "weekly":
                end_date = start_date + timedelta(weeks=1)
            elif player.type == "monthly":
                end_date = start_date + timedelta(days=30)
            elif player.type == "two_month":
                end_date = start_date + timedelta(days=60)
            elif player.type == "three_month":
                end_date = start_date + timedelta(days=90)
            elif player.type == "one_year":
                end_date = start_date + timedelta(days=365)
            else:
                end_date = start_date  # إذا النوع غير معروف

            # التحقق إذا انتهى الاشتراك
            if now > end_date:
                player.situation = False  # لازم يدفع من جديد
            else:
                player.situation = True   # اشتراكه لسه فعّال
            player.save()
    serializer = PlayerSerializer(player)
    return Response(
        {
            "message": "Login successful.",
            "player": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny])    
def add_player(request):
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Player added successfully", "data": serializer.data},
                        status=status.HTTP_200_OK)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


add_player = csrf_exempt(add_player)


@api_view(['GET'])
def get_players(request):
    players = Player.objects.all()

    now = datetime.now().date()

    for player in players:
        # تأكد أن عنده تاريخ بداية
        if player.date:
            start_date = player.date
            # نحسب المدة المسموحة حسب النوع
            if player.type == "weekly":
                end_date = start_date + timedelta(weeks=1)
            elif player.type == "monthly":
                end_date = start_date + timedelta(days=30)
            elif player.type == "two_month":
                end_date = start_date + timedelta(days=60)
            elif player.type == "three_month":
                end_date = start_date + timedelta(days=90)
            elif player.type == "one_year":
                end_date = start_date + timedelta(days=365)
            else:
                end_date = start_date  # إذا النوع غير معروف

            # التحقق إذا انتهى الاشتراك
            if now > end_date:
                player.situation = False  # لازم يدفع من جديد
            else:
                player.situation = True   # اشتراكه لسه فعّال
            player.save()

    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_player(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
        now = datetime.now().date()
        if player.date:
            start_date = player.date
            # نحسب المدة المسموحة حسب النوع
            if player.type == "weekly":
                end_date = start_date + timedelta(weeks=1)
            elif player.type == "monthly":
                end_date = start_date + timedelta(days=30)
            elif player.type == "two_month":
                end_date = start_date + timedelta(days=60)
            elif player.type == "three_month":
                end_date = start_date + timedelta(days=90)
            elif player.type == "one_year":
                end_date = start_date + timedelta(days=365)
            else:
                end_date = start_date  # إذا النوع غير معروف

            # التحقق إذا انتهى الاشتراك
            if now > end_date:
                player.situation = False  # لازم يدفع من جديد
            else:
                player.situation = True   # اشتراكه لسه فعّال
            player.save()
    except Player.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlayerSerializer(player)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([])            # تعطل SessionAuthentication -> لا حاجة لـ CSRF
@permission_classes([AllowAny])        # إذا أردت قيود لاحقاً غيّرها
def delete_player(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return Response({"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND)

    player.delete()
    return Response({"message": "Player deleted successfully."}, status=status.HTTP_200_OK)



@api_view(['PUT', 'PATCH'])
@authentication_classes([])      
@permission_classes([AllowAny])    
def update_player(request, player_id):
  
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return Response({"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND)

    partial = True if request.method == 'PATCH' else False

    serializer = PlayerSerializer(player, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Player updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


