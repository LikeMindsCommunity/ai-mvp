from typing import Dict, Any, Optional
from api.infrastructure.database import get_supabase_client
import httpx

async def create_project(user_id: str, name: str, description: Optional[str] = None) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        data = client.from_('projects').insert({
            'owner_id': user_id,
            'name': name,
            'description': description
        }).execute()
        return data
    except Exception as e:
        raise ValueError(f"Project creation error: {str(e)}")

async def get_projects(user_id: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        query = client.from_('projects').select('*').eq('owner_id', user_id)
        result = query.execute()
        return result
    except Exception as e:
        raise ValueError(f"Project retrieval error: {str(e)}")

async def get_project(project_id: str, user_id: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        query = client.from_('projects').select('*').eq('id', project_id).eq('owner_id', user_id)
        result = query.execute()
        if result.data:
            return result
        return result
    except Exception as e:
        raise ValueError(f"Project retrieval error: {str(e)}")

async def update_project(project_id: str, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
        if not owner_check.data:
            return {"data": None}
        result = client.from_('projects').update(data).eq('id', project_id).execute()
        return result
    except Exception as e:
        raise ValueError(f"Project update error: {str(e)}")

async def delete_project(project_id: str, user_id: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
        if not owner_check.data:
            return {"data": None}
        result = client.from_('projects').delete().eq('id', project_id).execute()
        return result
    except Exception as e:
        raise ValueError(f"Project deletion error: {str(e)}")

async def share_project(project_id: str, user_email: str, role: str, owner_id: str) -> Dict[str, Any]:
    client = get_supabase_client()
    try:
        owner_check = client.from_('projects').select('id').eq('id', project_id).eq('owner_id', owner_id).execute()
        if not owner_check.data:
            return {"data": None}
        user_result = client.from_('profiles').select('id').eq('email', user_email).execute()
        if not user_result.data:
            raise ValueError(f"User with email {user_email} not found")
        target_user_id = user_result.data[0]['id']
        existing_check = client.from_('project_members').select('*').eq('project_id', project_id).eq('user_id', target_user_id).execute()
        if existing_check.data:
            result = client.from_('project_members').update({
                'role': role,
                'updated_at': 'now()'
            }).eq('project_id', project_id).eq('user_id', target_user_id).execute()
        else:
            result = client.from_('project_members').insert({
                'project_id': project_id,
                'user_id': target_user_id,
                'role': role
            }).execute()
        return result
    except Exception as e:
        raise ValueError(f"Project sharing error: {str(e)}") 