from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from guest_list import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

photo_list = views.PhotoListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
guest_list = views.GuestViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# guest_by_details = views.GuestViewSet.as_view({
#     'get': 'get_by_details'
# })

guest_detail = views.GuestViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
photo_detail = views.PhotoListViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# urlpatterns = [
#     path('', views.api_root),
#     path('guests/', guest_list, name="guest-list"),
#     path('guests-by-details/', guest_by_details, name="guest-by-details"),
#     path('guests/<str:pk>/', guest_detail, name="guest-detail"),
# ]

urlpatterns = [
    path('', views.api_root),
    path('guests/', views.GuestList.as_view(), name="guest-list"),
    path('guests-internal/', guest_list, name="guest-list-internal"),
    path('guests/<str:pk>/', views.GuestDetail.as_view(), name="guest-details"),
    path('guests-internal/<str:pk>/', guest_detail, name="guest-details-internal"),
    path('guests-by-details/', views.GuestByKeyword.as_view(), name="guest-by-details"),
    path('photos/', views.PhotoList.as_view(), name="photo-list"),
    path('photos/internal/', photo_list, name="photo-list-internal"),
    path('photos/internal/<str:pk>/', photo_detail, name="photo-list-internal"),
    path('photos/carousel/', views.get_carousel, name="photo-carousel"),
    path('photos/event/', views.get_event_cover, name="photo-event"),
]

urlpatterns = format_suffix_patterns(urlpatterns)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)