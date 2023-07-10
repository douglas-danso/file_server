from django.urls import path
from fileapp import views
from .views import FileListView,FileDetailView

app_name = 'fileapp'

urlpatterns = [
    path('upload_file/', views.upload_file, name='upload_file'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
    path('send_file/<int:file_id>/', views.send_file_email, name='send_file_email'),
    path('files/', FileListView.as_view(), name='upload_list'),
    path('search/', views.search_view, name='search'),
    path('file/<int:pk>/', FileDetailView.as_view(), name='file_detail'),
    path('logs/', views.logs, name='logs'),
    path('preview/<int:file_id>/',views.preview,name = 'preview'),
    path('display/<int:file_id>/',views.open_page,name = 'open_page')
    ]