from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, HabitLogViewSet

router = DefaultRouter()

router.register("habits",HabitViewSet,basename="habit")
router.register("habit-logs", HabitLogViewSet, basename="habit-log")


urlpatterns = router.urls