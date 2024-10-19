
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Automated Evaluation System '
admin.site.site_title = 'Automated Evaluation System Final Year Project'
admin.site.index_title = 'Admin Dashboard'

urlpatterns = [
    path("admin/", admin.site.urls),

    path('',include('scorer.urls')),

]
