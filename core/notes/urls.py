from django.urls import path
from . import views


app_name = 'notes'

urlpatterns = [
    path('', views.NotesListCreateView.as_view(), name='list-create'),
    path('<int:id>', views.NotesUpdateDeleteView.as_view(), name='update-delete')
]