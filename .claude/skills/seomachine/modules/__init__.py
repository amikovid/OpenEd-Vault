# SEOMachine modules
# Import from vault .env for credentials

import os
from pathlib import Path

def load_env():
    """Load environment variables from vault .env file."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return  # dotenv not available, assume env vars already set

    # Find vault root (where .env lives)
    current = Path(__file__).resolve()
    for parent in current.parents:
        env_path = parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return

    # Fallback: try known location
    vault_env = Path.home() / "Desktop" / "New Root Docs" / "OpenEd Vault" / ".env"
    if vault_env.exists():
        load_dotenv(vault_env)

# Auto-load on import
load_env()
