from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('imagetext/', Image_Text.as_view(), name='image_upload'),
    path('summary/', Text_Summary.as_view(), name='summary'),
    path('audio/', Text_Audio.as_view(), name='audio'),
    path('paraphraser/', Text_Paraph.as_view(), name='paraph'),
    path('payment/', Payment.as_view(), name='payment'),
]