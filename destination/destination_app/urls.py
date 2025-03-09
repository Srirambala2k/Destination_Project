from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, AccountMemberViewSet, RoleViewSet, LogViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'members', AccountMemberViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'logs', LogViewSet)

urlpatterns = [
    path('/', include(router.urls)),
]

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
]   