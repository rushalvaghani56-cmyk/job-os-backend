"""Services package — business logic layer.

Only fully implemented services are exported here.
Stub services (NotImplementedError) are imported directly by route modules.
"""

from app.services import auth_service

__all__ = ["auth_service"]
