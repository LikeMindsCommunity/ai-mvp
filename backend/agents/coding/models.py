"""
Models for the Coding Agent service.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SDKContextModel(BaseModel):
    """SDK integration context for code generation."""
    component: str = Field(default="chat", description="SDK component to integrate (chat/feed)")
    version: str = Field(default="latest", description="SDK version to target")
    documentation: Optional[str] = Field(default=None, description="SDK documentation content")
    source_repo: Optional[str] = Field(default=None, description="Source repository URL")
    platform_config: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific config")

class CodingRequest(BaseModel):
    """
    A request to the Coding Agent.
    """
    requirements: str = Field(..., description="The user's requirements for code generation")
    platform: str = Field(..., description="The target platform (e.g., 'web', 'mobile', 'backend')")
    language: str = Field(..., description="The programming language to use")
    project_id: str = Field(..., description="Unique identifier for this project")
    output_dir: Optional[str] = Field(default=None, description="Optional custom output directory")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional additional context")
    solution_document: Optional[str] = Field(default=None, description="Solution document from documentation system")
    sdk_context: Optional[SDKContextModel] = Field(default=None, description="SDK-specific context")
    user_id: Optional[str] = Field(default=None, description="The ID of the user making the request")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata for the request"
    )

class FileInfo(BaseModel):
    """
    Information about a generated file.
    """
    path: str = Field(..., description="The relative path of the file")
    description: str = Field(..., description="Brief description of the file's purpose")
    content_preview: Optional[str] = Field(default=None, description="Preview of the file content")
    size: Optional[int] = Field(default=None, description="File size in bytes")
    language: Optional[str] = Field(default=None, description="Programming language of the file")
    sdk_components_used: Optional[List[str]] = Field(default=None, description="SDK components used in this file")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata about the file"
    )

class ValidationIssue(BaseModel):
    """
    An issue identified during code validation.
    """
    severity: str = Field(..., description="Severity level (error, warning, info)")
    message: str = Field(..., description="Description of the issue")
    file: Optional[str] = Field(default=None, description="Related file path")
    line: Optional[int] = Field(default=None, description="Line number in the file")
    code: Optional[str] = Field(default=None, description="Issue code or identifier")
    sdk_related: Optional[bool] = Field(default=False, description="Whether the issue is SDK-related")

class SDKValidationIssue(BaseModel):
    """
    SDK-specific validation issue.
    """
    type: str = Field(..., description="Issue type (initialization, authentication, etc)")
    severity: str = Field(..., description="Severity level")
    description: str = Field(..., description="Description of the issue")
    file: Optional[str] = Field(default=None, description="Related file path")
    line_reference: Optional[str] = Field(default=None, description="Method or line reference")
    correct_implementation: Optional[str] = Field(default=None, description="Example of correct implementation")

class ValidationResult(BaseModel):
    """
    Comprehensive validation results.
    """
    passes_all_requirements: bool = Field(..., description="Whether the code passes all requirements")
    average_score: float = Field(..., description="Average validation score (0-100)")
    issues: List[ValidationIssue] = Field(default_factory=list, description="General validation issues")
    sdk_score: Optional[int] = Field(default=None, description="SDK integration quality score (0-100)")
    sdk_validation_issues: Optional[List[SDKValidationIssue]] = Field(default=None, description="SDK validation issues")
    essential_files_missing: Optional[List[str]] = Field(default=None, description="Missing essential SDK files")
    integration_complete: Optional[bool] = Field(default=None, description="Whether SDK integration is complete")
    next_steps: Optional[List[str]] = Field(default=None, description="Suggested next steps")

class CodingResponse(BaseModel):
    """
    A response from the Coding Agent.
    """
    project_id: str = Field(..., description="The project ID")
    output_dir: str = Field(..., description="Directory containing the generated code")
    status: str = Field(..., description="Status of the generation (success, needs_review, error)")
    files: List[FileInfo] = Field(
        default_factory=list, description="Information about generated files"
    )
    complexity_estimate: Dict[str, Any] = Field(
        ..., description="Estimated complexity of the implementation"
    )
    validation: Optional[ValidationResult] = Field(
        default=None, description="Comprehensive validation results"
    )
    processing_time: float = Field(..., description="Time taken to process in seconds")
    error: Optional[str] = Field(default=None, description="Error message, if any")
    sdk_component: Optional[str] = Field(default=None, description="SDK component used")
    sdk_version: Optional[str] = Field(default=None, description="SDK version targeted")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata about the response"
    )
    progress_updates: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Progress updates during processing"
    )

class RefinementRequest(BaseModel):
    """
    Request to refine previously generated code.
    """
    project_id: str = Field(..., description="The ID of the previously generated project")
    feedback: str = Field(..., description="User feedback on the code")
    modifications: List[Dict[str, Any]] = Field(..., description="Specific modifications to make")
    output_dir: Optional[str] = Field(default=None, description="Output directory of the previous generation")
    sdk_context: Optional[SDKContextModel] = Field(default=None, description="Updated SDK context if any")

class ProgressUpdate(BaseModel):
    """
    Progress update during processing.
    """
    step: str = Field(..., description="Processing step identifier")
    percentage: float = Field(..., description="Completion percentage (0-1)")
    message: str = Field(..., description="Status message")
    timestamp: float = Field(..., description="Timestamp of the update")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional details") 