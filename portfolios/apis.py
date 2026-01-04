"""API endpoints using APIView classes.

This module contains API classes that handle HTTP requests. APIs should
be thin - they call services/selectors and serialize responses.

API classes should:
- Inherit from APIView (avoid generic views)
- Use nested InputSerializer and OutputSerializer
- Call services for write operations
- Call selectors for read operations
- Follow naming convention: <Entity><Action>Api (e.g., PortfolioListApi)
"""

