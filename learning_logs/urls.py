from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    #Domashnaya stranica
    path('', views.index, name='index'),

    #Vivod vsex tem
    path('topics/', views.topics, name = 'topics'),
    
    #stranica s podrobnoy inforaciey po otdelnoy teme
    path('topics/<int:topic_id>/', views.topic, name = 'topic'),

    #Strania dla dobavleniya novoy temi 
    path('new_topic/', views.new_topic, name='new_topic'),

    #Stranica dla dobavleniya  novoy zapisi
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),

    #Starnica dla redaktirovaniya zapisi
    path('edit_entry/<int:entry_id>/', views.edit_entry, name = 'edit_entry'),


]