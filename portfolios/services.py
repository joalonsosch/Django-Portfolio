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

