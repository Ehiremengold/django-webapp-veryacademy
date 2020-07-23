from rest_framework.routers import SimpleRouter

from .views import HustleViewSet

router = SimpleRouter()
router.register('hustle_posts', HustleViewSet)

urlpatterns = router.urls