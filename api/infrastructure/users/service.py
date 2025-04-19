from typing import Dict, Any
from api.infrastructure.database import get_supabase_client
import httpx

async def get_profile(jwt: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        client.auth.set_session(jwt)
        data = client.rpc('get_my_profile').execute()
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Profile retrieval error: {str(e)}")

async def update_profile(profile_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        client.auth.set_session(jwt)
        data = client.rpc('update_my_profile', profile_data).execute()
        return data
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Profile update error: {str(e)}") 