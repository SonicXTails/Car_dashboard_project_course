from main.models import CustomUser, Card
from .forms import CardForm, CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone

# ===== Профиль пользователя =====
@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)

    # Админ и аналитик не имеют доступа к профилю
    if request.user.role in ['admin', 'analyst']:
        return HttpResponseForbidden("У вас нет доступа к профилю")

    # Только владелец может редактировать свой профиль
    if request.user.id == profile_user.id and request.method == "POST":
        for field in ["user_type", "first_name", "last_name", "middle_name", "company_name", "phone"]:
            value = request.POST.get(field)
            if value:
                setattr(profile_user, field, value)
        profile_image = request.FILES.get("profile_image")
        if profile_image:
            profile_user.profile_image = profile_image
        profile_user.save()
        return redirect('profile', user_id=profile_user.id)

    cards = Card.objects.filter(user=profile_user).order_by('-created_at')
    return render(request, 'main/profile.html', {
        'profile_user': profile_user,
        'cards': cards,
    })


# ===== Регистрация =====
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, "main/register.html", {"form": form})


# ===== Логин =====
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, "main/login.html", {"form": form})


# ===== Логаут =====
def logout_view(request):
    logout(request)
    return redirect('/')


# ===== Главная =====
def home_view(request):
    cards = Card.objects.all().order_by('-created_at')
    return render(request, "main/home.html", {'cards': cards})


# ===== Создание карточки =====
@login_required
def create_card_view(request):
    if request.user.role in ['admin', 'analyst']:
        return HttpResponseForbidden("Вы не можете создавать карточки")

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('home')
    else:
        form = CardForm()
    return render(request, 'main/create_card.html', {'form': form})


# ===== Редактирование карточки =====
@login_required
def edit_card_view(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    # Только владелец может редактировать
    if card.user != request.user or request.user.role in ['admin', 'analyst']:
        return HttpResponseForbidden("Вы не можете редактировать эту карточку")

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CardForm(instance=card)
    return render(request, 'main/create_card.html', {'form': form, 'edit': True})


# ===== Удаление карточки =====
@login_required
def delete_card_view(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    # Только владелец может удалять
    if card.user != request.user or request.user.role in ['admin', 'analyst']:
        return HttpResponseForbidden("Вы не можете удалить эту карточку")

    if request.method == 'POST':
        card.delete()
        return redirect('home')
    return render(request, 'main/delete_card.html', {'card': card})


# ===== Панели =====
@login_required
def admin_panel_view(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Нет доступа к админ-панели")
    return render(request, 'main/admin_panel.html')


@login_required
def manager_panel_view(request):
    if request.user.role != 'analyst' and request.user.role != 'user':
        return HttpResponseForbidden("Нет доступа к панели менеджера")
    return render(request, 'main/manager_panel.html')


# ===== Детали карточки =====
def card_detail_view(request, pk):
    card = get_object_or_404(Card, pk=pk)
    user = card.user  

    days_on_site = (timezone.now() - user.date_joined).days

    context = {
        "card": card,
        "days_on_site": days_on_site,
        "seller": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "company_name": getattr(user, "company_name", None),
            "phone": getattr(user, "phone", None),
            "profile_image": getattr(user, "profile_image", None),
            "user_type": getattr(user, "user_type", "individual"),
            "date_joined": user.date_joined,
        }
    }
    return render(request, "main/card_detail.html", context)
