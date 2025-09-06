from main.models import CustomUser
from .forms import CardForm
from .models import Card
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Профиль пользователя
@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    
    # Запрет для admin и analyst
    if request.user.role in ['admin', 'analyst']:
        return HttpResponseForbidden("У вас нет доступа к профилю")

    # Только владелец может редактировать
    if request.user.id == profile_user.id:
        if request.method == "POST":
            user_type = request.POST.get("user_type", "")
            first_name = request.POST.get("first_name", "")
            last_name = request.POST.get("last_name", "")
            middle_name = request.POST.get("middle_name", "")
            company_name = request.POST.get("company_name", "")
            phone = request.POST.get("phone", "")
            profile_image = request.FILES.get("profile_image")

            if user_type:
                profile_user.user_type = user_type
            if first_name != "":
                profile_user.first_name = first_name
            if last_name != "":
                profile_user.last_name = last_name
            if middle_name != "":
                profile_user.middle_name = middle_name
            if company_name != "":
                profile_user.company_name = company_name
            if phone != "":
                profile_user.phone = phone
            if profile_image:
                profile_user.profile_image = profile_image

            profile_user.save()
            return redirect('profile', user_id=profile_user.id)

    cards = Card.objects.filter(user=profile_user).order_by('-created_at')

    return render(request, 'main/profile.html', {
        'profile_user': profile_user,
        'cards': cards,
    })

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

def logout_view(request):
    logout(request)
    return redirect('/')

def home_view(request):
    cards = Card.objects.all().order_by('-created_at')

    return render(request, "main/home.html", {
        'cards': cards
    })

@login_required
def create_card_view(request):
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

@login_required
def edit_card_view(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)  # только владелец
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CardForm(instance=card)
    return render(request, 'main/create_card.html', {'form': form, 'edit': True})

@login_required
def delete_card_view(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)  # только владелец
    if request.method == 'POST':
        card.delete()
        return redirect('home')
    return render(request, 'main/delete_card.html', {'card': card})


@login_required
def admin_panel_view(request):
    # Можно потом наполнить контентом
    return render(request, 'main/admin_panel.html')

@login_required
def manager_panel_view(request):
    # Можно потом наполнить контентом
    return render(request, 'main/manager_panel.html')

