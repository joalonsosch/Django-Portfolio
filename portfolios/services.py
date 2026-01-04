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
import logging
from decimal import Decimal
from datetime import date
from django.db import transaction
from .models import Asset, Portfolio, Price, PortfolioWeight, PortfolioHolding
from .selectors import portfolio_weight_list, price_get

logger = logging.getLogger(__name__)


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


@transaction.atomic
def portfolio_holding_create(
    *,
    portfolio: Portfolio,
    asset: Asset,
    date: date,
    quantity: Decimal
) -> PortfolioHolding:
    """Create a PortfolioHolding instance.
    
    Args:
        portfolio: Related Portfolio instance
        asset: Related Asset instance
        date: Holding date
        quantity: Quantity c_{i,t}
    
    Returns:
        Created or existing PortfolioHolding instance
    """
    holding, created = PortfolioHolding.objects.get_or_create(
        portfolio=portfolio,
        asset=asset,
        date=date,
        defaults={'quantity': quantity}
    )
    if not created:
        holding.quantity = quantity
        holding.full_clean()
        holding.save()
    return holding


@transaction.atomic
def portfolio_initial_quantities_calculate(
    *,
    portfolio: Portfolio
) -> dict[str, PortfolioHolding]:
    """Calculate and store initial quantities for a portfolio.
    
    Uses the formula: C_{i,0} = (w_{i,0} * V₀) / P_{i,0}
    
    Where:
    - w_{i,0} = initial weight of asset i (from PortfolioWeight)
    - V₀ = initial portfolio value
    - P_{i,0} = initial price of asset i on initial_date (from Price)
    - C_{i,0} = initial quantity of asset i
    
    Args:
        portfolio: Portfolio instance to calculate quantities for
    
    Returns:
        Dictionary mapping asset names to PortfolioHolding instances
    
    Raises:
        ValueError: If portfolio missing required data (initial_value, initial_date)
    """
    # Validate portfolio has required data
    if not portfolio.initial_value:
        raise ValueError(f"Portfolio {portfolio.name} missing initial_value")
    if not portfolio.initial_date:
        raise ValueError(f"Portfolio {portfolio.name} missing initial_date")
    
    V_0 = portfolio.initial_value
    initial_date = portfolio.initial_date
    holdings = {}
    
    # Get all weights for the portfolio
    weights = portfolio_weight_list(portfolio=portfolio)
    
    if not weights.exists():
        logger.warning(f"No weights found for portfolio {portfolio.name}")
        return holdings
    
    # Calculate quantity for each asset
    for weight in weights:
        asset = weight.asset
        w_i_0 = weight.initial_weight
        
        # Get initial price for asset on initial_date
        price_obj = price_get(asset=asset, date=initial_date)
        
        if price_obj is None:
            logger.warning(
                f"Price not found for asset {asset.name} on {initial_date}, skipping"
            )
            continue
        
        P_i_0 = price_obj.price
        
        # Validate price is positive (avoid division by zero)
        if P_i_0 <= 0:
            logger.warning(
                f"Invalid price {P_i_0} for asset {asset.name} on {initial_date}, skipping"
            )
            continue
        
        # Calculate quantity: C_{i,0} = (w_{i,0} * V₀) / P_{i,0}
        try:
            C_i_0 = (w_i_0 * V_0) / P_i_0
            
            # Validate quantity is positive
            if C_i_0 <= 0:
                logger.warning(
                    f"Calculated quantity {C_i_0} for asset {asset.name} is not positive, skipping"
                )
                continue
            
            # Create PortfolioHolding
            holding = portfolio_holding_create(
                portfolio=portfolio,
                asset=asset,
                date=initial_date,
                quantity=C_i_0
            )
            holdings[asset.name] = holding
            
        except Exception as e:
            logger.error(
                f"Error calculating quantity for asset {asset.name}: {str(e)}"
            )
            continue
    
    return holdings

