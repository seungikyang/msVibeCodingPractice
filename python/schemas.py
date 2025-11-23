from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class CreatePostRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username of the post author", json_schema_extra={"example": "johndoe"})
    content: str = Field(..., min_length=1, description="Content of the post", json_schema_extra={"example": "This is my first post about outdoor activities!"})


class UpdatePostRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username of the post author (for verification)", json_schema_extra={"example": "johndoe"})
    content: str = Field(..., min_length=1, description="Updated content of the post", json_schema_extra={"example": "This is my updated post about outdoor activities!"})


class Post(BaseModel):
    id: str = Field(..., description="Unique identifier of the post", json_schema_extra={"example": "post-123"})
    username: str = Field(..., description="Username of the post author", json_schema_extra={"example": "johndoe"})
    content: str = Field(..., description="Content of the post", json_schema_extra={"example": "This is my first post about outdoor activities!"})
    created_at: datetime = Field(alias="createdAt", description="Timestamp when the post was created", json_schema_extra={"example": "2025-05-30T10:30:00Z"})
    updated_at: datetime = Field(alias="updatedAt", description="Timestamp when the post was last updated", json_schema_extra={"example": "2025-05-30T11:45:00Z"})
    likes_count: int = Field(alias="likesCount", ge=0, description="Number of likes on the post", json_schema_extra={"example": 42})

    class Config:
        from_attributes = True
        populate_by_name = True


class CreateCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username of the comment author", json_schema_extra={"example": "janedoe"})
    content: str = Field(..., min_length=1, description="Content of the comment", json_schema_extra={"example": "Great post! I love outdoor activities too."})


class UpdateCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username of the comment author (for verification)", json_schema_extra={"example": "janedoe"})
    content: str = Field(..., min_length=1, description="Updated content of the comment", json_schema_extra={"example": "Great post! I really love outdoor activities."})


class Comment(BaseModel):
    id: str = Field(..., description="Unique identifier of the comment", json_schema_extra={"example": "comment-456"})
    post_id: str = Field(alias="postId", description="Unique identifier of the post this comment belongs to", json_schema_extra={"example": "post-123"})
    username: str = Field(..., description="Username of the comment author", json_schema_extra={"example": "janedoe"})
    content: str = Field(..., description="Content of the comment", json_schema_extra={"example": "Great post! I love outdoor activities too."})
    created_at: datetime = Field(alias="createdAt", description="Timestamp when the comment was created", json_schema_extra={"example": "2025-05-30T12:00:00Z"})
    updated_at: datetime = Field(alias="updatedAt", description="Timestamp when the comment was last updated", json_schema_extra={"example": "2025-05-30T12:30:00Z"})

    class Config:
        from_attributes = True
        populate_by_name = True


class LikeRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username of the user who wants to like the post", json_schema_extra={"example": "bobsmith"})


class Like(BaseModel):
    post_id: str = Field(alias="postId", description="Unique identifier of the liked post", json_schema_extra={"example": "post-123"})
    username: str = Field(..., description="Username of the user who liked the post", json_schema_extra={"example": "bobsmith"})
    created_at: datetime = Field(alias="createdAt", description="Timestamp when the like was created", json_schema_extra={"example": "2025-05-30T13:00:00Z"})

    class Config:
        from_attributes = True
        populate_by_name = True


class Error(BaseModel):
    error: str = Field(..., description="Error code or type", json_schema_extra={"example": "BadRequest"})
    message: str = Field(..., description="Human-readable error message", json_schema_extra={"example": "Missing required field 'username'"})
    details: Optional[str] = Field(None, description="Additional details about the error (optional)", json_schema_extra={"example": "The 'username' field is required but was not provided in the request body"})

