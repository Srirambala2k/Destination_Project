from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, AccountMemberViewSet, RoleViewSet, LogViewSet, UserListView, UserDetailView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'members', AccountMemberViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'logs', LogViewSet)



urlpatterns = [
    path('/', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),  
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'), 
]   