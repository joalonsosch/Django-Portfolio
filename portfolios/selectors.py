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

