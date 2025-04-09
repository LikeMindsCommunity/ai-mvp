from fastapi import APIRouter, HTTPException, Depends
from api.models.schemas import GenerateCodeRequest, GenerateCodeResponse
from api.services.generator import CodeGenerationService
from api.services.flutter import FlutterProjectManager

router = APIRouter()

async def get_code_generator():
    return CodeGenerationService()

async def get_flutter_manager():
    return FlutterProjectManager()

@router.post("/generate", response_model=GenerateCodeResponse)
async def generate_code(
    request: GenerateCodeRequest,
    code_generator: CodeGenerationService = Depends(get_code_generator),
    flutter_manager: FlutterProjectManager = Depends(get_flutter_manager)
):
    """Generate Flutter code from a prompt"""
    try:
        # Create or get project
        project_id = await flutter_manager.create_project(request.project_id)
        
        # Generate code
        success, code, errors = await code_generator.generate_code(request.prompt)
        if not success:
            return GenerateCodeResponse(
                success=False,
                project_id=project_id,
                errors=errors
            )
        
        # Update project with new code
        update_success, update_error = await flutter_manager.update_code(project_id, code)
        if not update_success:
            return GenerateCodeResponse(
                success=False,
                project_id=project_id,
                errors=[f"Failed to update project: {update_error}"]
            )
        
        return GenerateCodeResponse(
            success=True,
            code=code,
            project_id=project_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 