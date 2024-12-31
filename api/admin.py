from django.contrib import admin
from .models import Sport, League, Season, Keychain, DiscountCode, Sale, SaleItem
# Register your models here.

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'created_at')
    search_fields = ('name',)
    list_filter = ('sport',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'sport', 'start_year', 'end_year', 'created_at')
    search_fields = ('name',)
    list_filter = ('sport', 'league', 'start_year', 'end_year')


@admin.register(Keychain)
class KeychainAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('season',)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'total', 'created_at')
    list_filter = ('code', 'created_at')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'keychain', 'quantity', 'subtotal')
    search_fields = ('keychain__name',)
    list_filter = ('sale',)