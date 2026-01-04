"""Business logic for data fetching operations.

This module contains selector functions that handle reading and querying
data from the database. All data fetching logic should be placed here,
not in views or APIs.

Selector functions should:
- Use keyword-only arguments (*)
- Be type-annotated
- Use django-filter FilterSets for filtering
- Return QuerySets or lists
- Follow naming convention: <entity>_<action> (e.g., portfolio_list, portfolio_get)
"""
from datetime import date
from typing import Optional
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from .models import Asset, Portfolio, Price, PortfolioWeight


def portfolio_weight_get(
    *,
    portfolio: Portfolio,
    asset: Asset
) -> Optional[PortfolioWeight]:
    """Get PortfolioWeight for a specific portfolio and asset.
    
    Args:
        portfolio: Portfolio instance
        asset: Asset instance
    
    Returns:
        PortfolioWeight instance or None if not found
    """
    try:
        return PortfolioWeight.objects.get(portfolio=portfolio, asset=asset)
    except ObjectDoesNotExist:
        return None


def price_get(
    *,
    asset: Asset,
    date: date
) -> Optional[Price]:
    """Get Price for a specific asset and date.
    
    Args:
        asset: Asset instance
        date: Price date
    
    Returns:
        Price instance or None if not found
    """
    try:
        return Price.objects.get(asset=asset, date=date)
    except ObjectDoesNotExist:
        return None


def portfolio_weight_list(
    *,
    portfolio: Portfolio
) -> QuerySet[PortfolioWeight]:
    """Get all weights for a portfolio.
    
    Args:
        portfolio: Portfolio instance
    
    Returns:
        QuerySet of PortfolioWeight instances
    """
    return PortfolioWeight.objects.filter(portfolio=portfolio).select_related('asset')

