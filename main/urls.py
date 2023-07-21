from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'fields', FieldViewSet)
router.register(r'fieldstypes', FieldTypeViewSet, 'fieldstypes-detail')
router.register(r'requests', RequestViewSet, 'request-detail')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('send-otp/', SendOTPApiView.as_view()),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('user-info/', GetUserInfo.as_view()),
    path('find-user/', FindUserByPhone.as_view()),
    path('change-password/', ChangeUserPassword.as_view()),
]
