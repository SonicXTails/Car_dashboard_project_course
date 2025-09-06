from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserProfileSerializer, UserReviewSerializer, CardSerializer
from django.contrib.auth import authenticate, login, logout
from main.models import CustomUser, Card, UserReview

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
    

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile_api(request):
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Получить все отзывы о пользователе
@api_view(["GET"])
def user_reviews_list(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

    reviews = UserReview.objects.filter(reviewed=user)
    serializer = UserReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# Добавить или обновить отзыв
@api_view(["POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_review(request, user_id):
    try:
        reviewed_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.id == reviewed_user.id:
        return Response({"message": "Нельзя оставить отзыв самому себе"}, status=status.HTTP_200_OK)
    try:
        review = UserReview.objects.get(reviewer=request.user, reviewed=reviewed_user)
    except UserReview.DoesNotExist:
        review = None

    # POST — создать отзыв
    if request.method == "POST":
        if review:
            return Response({"detail": "Вы уже оставили отзыв."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user, reviewed=reviewed_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT — редактирование отзыва
    if request.method == "PUT":
        if not review:
            return Response({"detail": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE — удалить отзыв
    if request.method == "DELETE":
        if not review:
            return Response({"detail": "Отзыв не найден"}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({"message": "Отзыв удален"}, status=status.HTTP_204_NO_CONTENT)