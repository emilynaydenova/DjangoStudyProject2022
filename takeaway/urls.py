from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Takeaway Administration'
admin.site.site_title = 'Takeaway Site Admin'
admin.site.index_title = 'Admin Home'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
   ]


