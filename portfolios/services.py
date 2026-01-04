"""Business logic for write operations.

This module contains service functions that handle creating, updating,
and deleting operations. All business logic for write operations should
be placed here, not in models, views, or APIs.

Service functions should:
- Use keyword-only arguments (*)
- Be type-annotated
- Use @transaction.atomic decorator when needed
- Call obj.full_clean() before saving
- Follow naming convention: <entity>_<action> (e.g., portfolio_create)
"""
from decimal import Decimal
from datetime import date
from django.db import transaction
from .models import Asset, Portfolio, Price, PortfolioWeight


@transaction.atomic
def asset_create(
    *,
    name: str,
    symbol: str | None = None
) -> Asset:
    """Create an Asset instance.
    
    Args:
        name: Asset name (e.g., 'EEUU', 'Europa')
        symbol: Optional symbol/ticker
    
    Returns:
        Created Asset instance
    """
    asset, created = Asset.objects.get_or_create(
        name=name,
        defaults={'symbol': symbol}
    )
    if not created and symbol:
        asset.symbol = symbol
        asset.full_clean()
        asset.save()
    return asset


@transaction.atomic
def portfolio_create(
    *,
    name: str,
    initial_value: Decimal,
    initial_date: date
) -> Portfolio:
    """Create a Portfolio instance.
    
    Args:
        name: Portfolio name (e.g., 'Portfolio 1', 'Portfolio 2')
        initial_value: Initial portfolio value V₀ in dollars
        initial_date: Initial date
    
    Returns:
        Created Portfolio instance
    """
    portfolio, created = Portfolio.objects.get_or_create(
        name=name,
        defaults={
            'initial_value': initial_value,
            'initial_date': initial_date
        }
    )
    if not created:
        portfolio.initial_value = initial_value
        portfolio.initial_date = initial_date
        portfolio.full_clean()
        portfolio.save()
    return portfolio


@transaction.atomic
def price_create(
    *,
    asset: Asset,
    date: date,
    price: Decimal
) -> Price:
    """Create a Price instance.
    
    Args:
        asset: Related Asset instance
        date: Price date
        price: Asset price p_{i,t}
    
    Returns:
        Created or existing Price instance
    """
    price_obj, created = Price.objects.get_or_create(
        asset=asset,
        date=date,
        defaults={'price': price}
    )
    if not created:
        price_obj.price = price
        price_obj.full_clean()
        price_obj.save()
    return price_obj


@transaction.atomic
def portfolio_weight_create(
    *,
    portfolio: Portfolio,
    asset: Asset,
    initial_weight: Decimal
) -> PortfolioWeight:
    """Create a PortfolioWeight instance.
    
    Args:
        portfolio: Related Portfolio instance
        asset: Related Asset instance
        initial_weight: Initial weight w_{i,0} as decimal (e.g., 0.15 for 15%)
    
    Returns:
        Created or existing PortfolioWeight instance
    """
    weight, created = PortfolioWeight.objects.get_or_create(
        portfolio=portfolio,
        asset=asset,
        defaults={'initial_weight': initial_weight}
    )
    if not created:
        weight.initial_weight = initial_weight
        weight.full_clean()
        weight.save()
    return weight

