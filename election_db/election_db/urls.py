
from django.contrib import admin
from django.urls import path
from web_interface.views import base_page, content_section, pie_chart_view, group_section, base_group, svg_test
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_page, name='base'),
    path('<str:group_name>/<str:item_name>/', content_section, name='content'),
    path('chart', pie_chart_view, name='chart'),
    # path('<str:group_name>/<str:item_name>/group', group_section, name='group'),
    path('gr', base_group, name='basegrouping'),
    path('svg', svg_test, name='svg_test'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
