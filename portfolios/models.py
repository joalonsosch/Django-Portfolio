from datetime import date
from django.db import models
from django.db.models import Q
from django.utils import timezone


class BaseModel(models.Model):
    """Base model with created_at and updated_at fields.
    
    All models in the application should inherit from this base model
    to ensure consistent timestamp tracking.
    """
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Asset(BaseModel):
    """Represents an investable asset.
    
    There are 17 investable assets in the system.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Asset name (e.g., 'EEUU', 'Europa')")
    symbol = models.CharField(max_length=20, blank=True, null=True, help_text="Optional symbol/ticker")
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
    
    def __str__(self):
        return self.name


class Portfolio(BaseModel):
    """Represents a portfolio (Portfolio 1 or Portfolio 2).
    
    Each portfolio has an initial value V₀ and initial date.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Portfolio name (e.g., 'Portfolio 1', 'Portfolio 2')")
    initial_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=1000000000.00,
        help_text="Initial portfolio value V₀ in dollars"
    )
    initial_date = models.DateField(
        default=date(2022, 2, 15),
        help_text="Initial date (15/02/22)"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'
    
    def __str__(self):
        return self.name


class Price(BaseModel):
    """Stores historical prices for each asset.
    
    Represents p_{i,t} - the price of asset i at time t.
    """
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='prices',
        help_text="Related asset"
    )
    date = models.DateField(db_index=True, help_text="Price date")
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Asset price p_{i,t}"
    )
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['asset', 'date']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['asset', 'date'],
                name='unique_asset_date_price'
            ),
            models.CheckConstraint(
                check=Q(price__gt=0),
                name='price_positive'
            ),
        ]
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
    
    def __str__(self):
        return f"{self.asset.name} - {self.date}: ${self.price}"


class PortfolioWeight(BaseModel):
    """Stores initial weights for assets in portfolios.
    
    Represents w_{i,0} - the initial weight of asset i in a portfolio.
    Weight is stored as a decimal (e.g., 0.15 for 15%).
    """
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='weights',
        help_text="Related portfolio"
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='portfolio_weights',
        help_text="Related asset"
    )
    initial_weight = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        help_text="Initial weight w_{i,0} as decimal (e.g., 0.15 for 15%)"
    )
    
    class Meta:
        ordering = ['portfolio', 'asset']
        constraints = [
            models.UniqueConstraint(
                fields=['portfolio', 'asset'],
                name='unique_portfolio_asset_weight'
            ),
            models.CheckConstraint(
                check=Q(initial_weight__gte=0) & Q(initial_weight__lte=1),
                name='weight_range_0_to_1'
            ),
        ]
        verbose_name = 'Portfolio Weight'
        verbose_name_plural = 'Portfolio Weights'
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name}: {self.initial_weight * 100:.2f}%"


class PortfolioHolding(BaseModel):
    """Tracks quantities held over time.
    
    Represents c_{i,t} - the quantity of asset i held in a portfolio at time t.
    This model is essential for time-series tracking, especially for Bonus 2 transaction processing.
    """
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='holdings',
        help_text="Related portfolio"
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='portfolio_holdings',
        help_text="Related asset"
    )
    date = models.DateField(db_index=True, help_text="Holding date")
    quantity = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        help_text="Quantity c_{i,t}"
    )
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['portfolio', 'asset', 'date']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['portfolio', 'asset', 'date'],
                name='unique_portfolio_asset_date_holding'
            ),
            models.CheckConstraint(
                check=Q(quantity__gte=0),
                name='quantity_non_negative'
            ),
        ]
        verbose_name = 'Portfolio Holding'
        verbose_name_plural = 'Portfolio Holdings'
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} ({self.date}): {self.quantity}"


class Transaction(BaseModel):
    """Stores buy/sell transactions.
    
    Used for Bonus 2: transaction processing.
    """
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="Related portfolio"
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="Related asset"
    )
    date = models.DateField(db_index=True, help_text="Transaction date")
    transaction_type = models.CharField(
        max_length=4,
        choices=TRANSACTION_TYPES,
        help_text="Transaction type: Buy or Sell"
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Transaction amount in dollars"
    )
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['portfolio', 'date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name='transaction_amount_positive'
            ),
        ]
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.get_transaction_type_display()} {self.asset.name} ({self.date}): ${self.amount}"
