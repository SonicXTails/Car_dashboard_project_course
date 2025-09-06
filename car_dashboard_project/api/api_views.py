from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from main.models import CustomUser, Card
from .serializers import CardSerializer

# Получение списка пользователей (только для админа)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_list(request):
    if not request.user.is_staff:
        return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Создание пользователя
@api_view(["POST"])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "Пользователь создан", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Логин через API
@api_view(["POST"])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)
        return Response({"message": "Успешный вход", "username": user.username})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Логаут через API
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({"message": "Вы вышли из системы"})

# Получение, обновление, удаление конкретного пользователя
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_detail_api(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

    # GET — получение данных
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

# PUT — обновление (админ или владелец)
    if request.method == "PUT":
        if not (request.user.is_staff or request.user.id == user.id):
            return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE — удаление (только для админа)
    if request.method == "DELETE":
        if not request.user.is_staff:
            return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({"message": "Пользователь удален"}, status=status.HTTP_204_NO_CONTENT)


# Список всех карточек
@api_view(["GET"])
def cards_list(request):
    cards = Card.objects.all().order_by('-created_at')
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)

# Создание карточки (только для авторизованного пользователя)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_card_api(request):
    serializer = CardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Детали, редактирование, удаление конкретной карточки
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def card_detail_api(request, card_id):
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return Response({"detail": "Карточка не найдена"}, status=status.HTTP_404_NOT_FOUND)

    # GET — получение данных
    if request.method == "GET":
        serializer = CardSerializer(card)
        return Response(serializer.data)

    # PUT — обновление (только владелец)
    if request.method == "PUT":
        if card.user != request.user:
            return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE — удаление (только владелец)
    if request.method == "DELETE":
        if card.user != request.user:
            return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
        card.delete()
        return Response({"message": "Карточка удалена"}, status=status.HTTP_204_NO_CONTENT)