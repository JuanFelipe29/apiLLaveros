from django.db import models

# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class League(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Keychain(models.Model):
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='keychains/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (0-100)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.value}%)"


class Sale(models.Model):
    code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - Total: ${self.total}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    keychain = models.ForeignKey(Keychain, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.keychain.name}"