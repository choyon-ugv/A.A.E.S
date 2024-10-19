from django.urls import path 
from .views import * 

urlpatterns = [
    path('',home,name='home'),
    path('exam/',take_test,name='take_test'),
    # path('check/',check_answer,name='check_answer'),
    path('check-result/<int:id>/',evaluate,name='check_result'),

    path('store-marks/<int:id>/',evaluate_and_store,name='store_marks'),

    path('permissions/',second_time,name='second_time')

]