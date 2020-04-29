from django.contrib import admin
from django.urls import path
from tours.views import MainView, DepartureView, TourView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('departure/<str:departure_city>/', DepartureView.as_view(), name='show_departure'),
    path('tour/<int:id>/', TourView.as_view()),
    path('', MainView.as_view()),    
]
