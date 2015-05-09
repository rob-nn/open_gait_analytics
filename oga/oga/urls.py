from django.conf.urls import include, url
from django.contrib import admin
from oga_webapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'gait_samples', views.GaitSampleViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'oga.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
