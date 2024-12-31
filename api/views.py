from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Sport, League, Season, Keychain, DiscountCode, Sale
from .serializers import (
    SportReadSerializer, SportWriteSerializer,
    LeagueReadSerializer, LeagueWriteSerializer,
    SeasonReadSerializer, SeasonWriteSerializer,
    KeychainReadSerializer, KeychainWriteSerializer,
    DiscountCodeReadSerializer, DiscountCodeWriteSerializer,
    SaleReadSerializer, SaleWriteSerializer
)


class SportViewSet(ModelViewSet):
    queryset = Sport.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SportWriteSerializer
        return SportReadSerializer


class LeagueViewSet(ModelViewSet):
    queryset = League.objects.select_related('sport').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sport']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LeagueWriteSerializer
        return LeagueReadSerializer


class SeasonViewSet(ModelViewSet):
    queryset = Season.objects.select_related('sport', 'league').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sport', 'league']
    search_fields = ['name']
    ordering_fields = ['name', 'start_year', 'end_year', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SeasonWriteSerializer
        return SeasonReadSerializer


class KeychainViewSet(ModelViewSet):
    queryset = Keychain.objects.select_related('season').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['season']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KeychainWriteSerializer
        return KeychainReadSerializer


class DiscountCodeViewSet(ModelViewSet):
    queryset = DiscountCode.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'value', 'is_active']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DiscountCodeWriteSerializer
        return DiscountCodeReadSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.prefetch_related('items__keychain', 'code').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['code']
    ordering_fields = ['created_at', 'total']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SaleWriteSerializer
        return SaleReadSerializer
