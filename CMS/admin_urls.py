from django.contrib import admin, sitemaps
from django.urls import path, include
from django.conf.urls.static import static
from CMS import settings
from CMS import views

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('add-destination/<str:faculty_pincode>/', views.add_destination),
    path('add-faculty-member/<str:faculty_pincode>/', views.add_faculty_members),
    path('test/', views.test),
    path('', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Courier Management System Administration'
admin.site.index_title = 'Manage the Site'
