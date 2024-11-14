from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = router.urls