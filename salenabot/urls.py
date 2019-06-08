from django.urls import path, include

from . import views
from salenabot.captioning_module.model_loader import load_model
urlpatterns = [
    path('', views.index, name='index'),
    path('wrtie_captured_img', views.wrtie_captured_img, name='wrtie_captured_img'),
    path('get_calling_user_caption', views.get_calling_user_caption, name='get_calling_user_caption'),
    path('get_recommendation_data', views.get_recommended_product_data, name='get_recommended_product_data'),

]
load_model()