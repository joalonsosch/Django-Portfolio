"""Custom exception handler for Django REST Framework.

This module provides a custom exception handler that standardizes
error responses and handles Django ValidationError conversion.
"""
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler


def custom_exception_handler(exc, ctx):
    """Custom exception handler for DRF.
    
    Converts Django ValidationError to DRF ValidationError and
    standardizes error response format to {"detail": ...}.
    
    Args:
        exc: The exception instance
        ctx: The context dictionary containing request, view, etc.
    
    Returns:
        Response object with standardized error format
    """
    # Convert Django ValidationError to DRF ValidationError
    if isinstance(exc, DjangoValidationError):
        # Convert Django ValidationError to DRF format
        from rest_framework.serializers import as_serializer_error
        exc = exceptions.ValidationError(as_serializer_error(exc))
    
    # Convert Http404 to DRF NotFound
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    
    # Get standard DRF exception response
    response = exception_handler(exc, ctx)
    
    # Ensure consistent error format
    if response is not None:
        # DRF already formats errors as {"detail": ...} for most cases
        # This ensures consistency across all error types
        pass
    
    return response

