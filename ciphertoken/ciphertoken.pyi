from typing import Any, Dict, Optional, Tuple

# CipherToken class stub
class CipherToken:
    """
    High-performance JWT token handler with support for multiple algorithms.
    
    Can be used in multiple ways:
    - Instance methods: ct.access(payload), ct.refresh(payload)
    - Module functions: access(ct, payload), refresh(ct, payload)
    - Direct create_token: ct.create_token(ttl_time, token_type, payload)
    """
    
    # Constructor
    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        access_ttl: int = 3600,
        refresh_ttl: int = 604800,
    ) -> None: ...
    
    # Properties (read-only)
    @property
    def secret(self) -> str:
        """Returns masked secret (first 8 chars + '...') for security."""
        ...
    
    @property
    def access_ttl(self) -> int:
        """Access token TTL in seconds."""
        ...
    
    @property
    def refresh_ttl(self) -> int:
        """Refresh token TTL in seconds."""
        ...
    
    # Token creation methods
    def create_token(
        self,
        ttl_time: int = 3153600000,
        token_type: str = "jwt",
        payload: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Core token creation with custom TTL and type.
        
        Args:
            ttl_time: Time-to-live in seconds (default: 3153600000 ~ 100 years)
            token_type: Token type identifier ("access" or "refresh")
            payload: Custom claims to include in token
        """
        ...
    
    def payload(self, payload: Optional[Dict[str, Any]] = None) -> str:
        """Create a generic access token (alias for access())."""
        ...
    
    def access(self, payload: Optional[Dict[str, Any]] = None) -> str:
        """Create an access token using access_ttl."""
        ...
    
    def refresh(self, payload: Optional[Dict[str, Any]] = None) -> str:
        """Create a refresh token using refresh_ttl."""
        ...
    
    async def access_async(self, payload: Optional[Dict[str, Any]] = None) -> str: ...
    async def refresh_async(self, payload: Optional[Dict[str, Any]] = None) -> str: ...
    
    # Token verification methods
    def decode(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate a token.
        
        Raises ValueError if token is invalid.
        """
        ...
    
    def verify(self, token: str) -> bool:
        """Check signature and expiry. Returns True if valid, False otherwise."""
        ...
    
    def inspect(self, token: str) -> Dict[str, Any]:
        """Decode without strict signature or expiry validation (for debugging)."""
        ...
    
    def remaining_time(self, token: str) -> Optional[int]:
        """Seconds until token expiry, or None."""
        ...
    
    # Token rotation
    def rotation(
        self, refresh_token: str, payload: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str]:
        """
        Rotate a refresh token into a new access + refresh pair.
        
        Raises ValueError if provided token is not a refresh token.
        """
        ...
    
    async def rotation_async(
        self, refresh_token: str, payload: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str]: ...
    
    # Utility
    def algorithm_name(self) -> str:
        """Current algorithm name (e.g., 'HS256', 'RS256')."""
        ...


def is_jwt_format(token: str) -> bool:
    """Check if string has valid JWT format (3 dot-separated parts)."""
    ...


def validate_jwt_format(token: str) -> bool:
    """Validate JWT format or raise ValueError."""
    ...