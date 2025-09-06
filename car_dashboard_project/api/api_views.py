from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from main.models import CustomUser, Card, UserReview, AdminLog
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserReviewSerializer, CardSerializer

# ===== Пользователи =====
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_list(request):
    if request.user.role != 'admin': return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
    return Response(UserSerializer(CustomUser.objects.all(), many=True).data)

@api_view(["POST"])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if getattr(request.user, 'role', None) == 'admin':
            AdminLog.objects.create(admin=request.user, action='create', target_table='CustomUser', target_id=user.id)
        return Response({"message": "Пользователь создан", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        login(request, serializer.validated_data)
        return Response({"message": "Успешный вход", "username": serializer.validated_data.username})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({"message": "Вы вышли из системы"})

@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_modify_api(request):
    user = get_object_or_404(CustomUser, id=request.data.get("id"))
    if request.method == "PUT":
        if request.user.role != 'admin' and request.user.id != user.id: return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if request.user.role == 'admin': AdminLog.objects.create(admin=request.user, action='update', target_table='CustomUser', target_id=user.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.user.role != 'admin': return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
    AdminLog.objects.create(admin=request.user, action='delete', target_table='CustomUser', target_id=user.id)
    user.delete()
    return Response({"message": "Пользователь удален"}, status=status.HTTP_204_NO_CONTENT)


# ===== Карточки =====
@api_view(["GET"])
def cards_list(request): return Response(CardSerializer(Card.objects.all().order_by('-created_at'), many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_card_api(request):
    serializer = CardSerializer(data=request.data)
    if serializer.is_valid():
        card = serializer.save(user=request.user)
        if request.user.role == 'admin': AdminLog.objects.create(admin=request.user, action='create', target_table='Card', target_id=card.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def card_modify_api(request):
    card = get_object_or_404(Card, id=request.data.get("id"))
    if request.method == "PUT":
        if card.user != request.user and request.user.role != 'admin': return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if request.user.role == 'admin': AdminLog.objects.create(admin=request.user, action='update', target_table='Card', target_id=card.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if card.user != request.user and request.user.role != 'admin': return Response({"detail": "Нет доступа"}, status=status.HTTP_403_FORBIDDEN)
    if request.user.role == 'admin': AdminLog.objects.create(admin=request.user, action='delete', target_table='Card', target_id=card.id)
    card.delete()
    return Response({"message": "Карточка удалена"}, status=status.HTTP_204_NO_CONTENT)


# ===== Отзывы =====
@api_view(["GET"])
def user_reviews_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return Response(UserReviewSerializer(UserReview.objects.filter(reviewed=user), many=True).data)

@api_view(["POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_review(request, user_id=None, review_id=None):
    if request.method == "POST":
        reviewed_user = get_object_or_404(CustomUser, id=user_id)
        if request.user.id == reviewed_user.id: return Response({"detail": "Нельзя оставить отзыв самому себе"}, status=status.HTTP_400_BAD_REQUEST)
        if UserReview.objects.filter(reviewer=request.user, reviewed=reviewed_user).exists(): return Response({"detail": "Вы уже оставили отзыв."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user, reviewed=reviewed_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    rid = review_id or request.data.get("id")
    review = get_object_or_404(UserReview, id=rid)
    if request.method == "PUT":
        serializer = UserReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(): serializer.save(); return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    review.delete()
    return Response({"message": "Отзыв удален"}, status=status.HTTP_204_NO_CONTENT)
