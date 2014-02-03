from rest_framework import routers

from .views import TweetViewSet


router = routers.DefaultRouter()
router.register(r'tweets', TweetViewSet, base_name='tweets')
urlpatterns = router.urls
