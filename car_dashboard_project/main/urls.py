from django.urls import path
from .views import home_view, profile_view, create_card_view
from .views import edit_card_view, delete_card_view, admin_panel_view, manager_panel_view, card_detail_view
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),

    path('', home_view, name='home'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('cards/create/', create_card_view, name='create_card'),
    path('cards/<int:card_id>/edit/', edit_card_view, name='edit_card'),
    path('cards/<int:card_id>/delete/', delete_card_view, name='delete_card'),

    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('manager-panel/', manager_panel_view, name='manager_panel'),

    path('cards/<int:card_id>/', card_detail_view, name='card_detail'),

]