from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

# Configure HTTPBearer security scheme with better description
security = HTTPBearer(
    scheme_name="Admin Bearer Token",
    description="Enter your admin token (the token will be automatically prefixed with 'Bearer')",
    auto_error=True
)


def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authorization credentials missing"
        )

    token = credentials.credentials
    if token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin token"
        )

    return True


# Dependency for admin routes
AdminAuth = Depends(verify_admin_token)
