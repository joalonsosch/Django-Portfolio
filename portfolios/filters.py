"""django-filter FilterSets for selectors.

This module contains FilterSet classes used by selectors for filtering
querysets. All filtering logic should be defined here and used within
selectors, not in views or APIs.

FilterSets should:
- Inherit from django_filters.FilterSet
- Be used within selector functions
- Follow naming convention: <Entity>Filter (e.g., PortfolioFilter)
"""

