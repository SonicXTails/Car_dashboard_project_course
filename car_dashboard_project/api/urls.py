from django.urls import path 
from . import api_views 
from django.conf import settings 
from django.conf.urls.static  import static

urlpatterns = [ 
    path('register/', api_views.register_api, name='api_register'), 
    path('login/', api_views.login_api, name='api_login'), 
    path('logout/', api_views.logout_api, name='api_logout'), 
    path('users/', api_views.users_list, name='api_users_list'), 
    path('users/modify/', api_views.user_modify_api, name='api_user_modify'), 
    path('cards/', api_views.cards_list, name='api_cards_list'), 
    path('cards/create/', api_views.create_card_api, name='api_create_card'), 
    path('cards/modify/', api_views.card_modify_api, name='api_card_modify'), 
    path('users/<int:user_id>/reviews/', api_views.user_reviews_list, name='user_reviews_list_api'), 
    path('users/<int:user_id>/review/', api_views.manage_review, name='manage_review_api'), 
    path('users/<int:user_id>/review/<int:review_id>/', api_views.manage_review, name='manage_review_detail_api'), ] 
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)