"""Messenger FastAPI application package.

Exposes common submodules for convenience and sets package version.
"""

__version__ = "0.1.0"

# Re-export commonly used submodules for easier access when importing from app
__all__ = [
	"auth",
	"config",
	"database",
	"models",
	"schemas",
]


