from django.db import models
import constants

# Create your models here.

class FiatCurrency(models.Model):
    """
    Description: Fiat currency
    """

    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    symbol = models.CharField(max_length=5, unique=True)
    in_EUR = models.DecimalField(max_digits=16, decimal_places=8)

    class Meta:
        pass

class FiatRateHistory(models.Model):
    """
    Description: Model Description
    """

    created_at = models.DateTimeField(auto_now_add=True)
    
    base = models.ForeignKey('FiatCurrency')
    target = models.ForeignKey('FiatCurrency')
    rate = models.DecimalField(max_digits=16, decimal_places=8)

    class Meta:
        pass


class CryptoAsset(models.Model):
    """
    Description: Model Description
    """
    
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    symbol = models.CharField(max_length=5, unique=True)
    in_USD = models.DecimalField(max_digits=16, decimal_places=8)

    class Meta:
        pass

    class Meta:
        pass


class CryptoRateHistory(models.Model):
    """
    Description: Model Description
    """

    created_at = models.DateTimeField(auto_now_add=True)
    
    base = models.ForeignKey('FiatCurrency')
    target = models.ForeignKey('CryptoAsset')
    rate = models.DecimalField(max_digits=16, decimal_places=8)

    class Meta:
        pass