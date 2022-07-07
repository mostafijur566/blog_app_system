from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', GetStatusView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('login/', obtain_auth_token),

    path('get-user/', get_user),
    path('get-other-user/<str:pk>/', get_other_user),

    path('get-categories/', get_all_categories),

    path('post-blog/', post_blog),
    path('get-blog/', get_blog),
    path('update-blog/<str:pk>/', update_blog),
    path('get-single-blog/<str:pk>/', get_single_blog),
    path('delete-post/<str:pk>/', delete_post),
    path('get-user-blog/', get_user_blog),
    path('get-post-by-category/<str:pk>/', get_post_by_category),
    path('get-filter-post/<str:pk>/', get_filter_post),

    path('post-comment/', post_comment),
    path('get-comment/<str:pk>/', get_comment),
    path('delete-comment/<str:pk>/', delete_comment),
]
