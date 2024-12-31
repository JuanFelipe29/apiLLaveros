from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SportViewSet, LeagueViewSet, SeasonViewSet, KeychainViewSet, DiscountCodeViewSet, SaleViewSet

# Configuración del enrutador
router = DefaultRouter()
router.register('sports', SportViewSet)
router.register('leagues', LeagueViewSet)
router.register('seasons', SeasonViewSet)
router.register('keychains', KeychainViewSet)
router.register('discount-codes', DiscountCodeViewSet)
router.register('sales', SaleViewSet)

# URLs principales
urlpatterns = [
    path('', include(router.urls)),
]
