from django.urls import path
from metal.views import MetalPrice

urlpatterns = [
    path('metal-prices', MetalPrice.as_view()),
]
