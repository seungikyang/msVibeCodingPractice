import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "",
    response_model=list[schemas.Post],
    summary="Get all posts",
    description="Retrieve a list of all recent posts",
    operation_id="listPosts",
    responses={
        500: {
            "description": "Internal server error",
            "model": schemas.Error
        }
    }
)
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    result = []
    for post in posts:
        likes_count = db.query(models.Like).filter(models.Like.post_id == post.id).count()
        post_dict = {
            "id": post.id,
            "username": post.username,
            "content": post.content,
            "createdAt": post.created_at,
            "updatedAt": post.updated_at,
            "likesCount": likes_count
        }
        result.append(schemas.Post(**post_dict))
    return result


@router.post(
    "",
    response_model=schemas.Post,
    status_code=201,
    summary="Create a new post",
    description="Create a new post with username and content",
    operation_id="createPost",
    responses={
        400: {
            "description": "Bad request - invalid input or missing required fields",
            "model": schemas.Error
        },
        500: {
            "description": "Internal server error",
            "model": schemas.Error
        }
    }
)
def create_post(post_data: schemas.CreatePostRequest, db: Session = Depends(get_db)):
    if not post_data.username or not post_data.content:
        raise HTTPException(status_code=400, detail="Missing required field")
    
    post_id = f"post-{uuid.uuid4().hex[:8]}"
    new_post = models.Post(
        id=post_id,
        username=post_data.username,
        content=post_data.content
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return schemas.Post(
        id=new_post.id,
        username=new_post.username,
        content=new_post.content,
        createdAt=new_post.created_at,
        updatedAt=new_post.updated_at,
        likesCount=0
    )


@router.get(
    "/{postId}",
    response_model=schemas.Post,
    summary="Get a single post",
    description="Retrieve details of a specific post by its ID",
    operation_id="getPost",
    responses={
        404: {
            "description": "Resource not found",
            "model": schemas.Error
        },
        500: {
            "description": "Internal server error",
            "model": schemas.Error
        }
    }
)
def get_post(postId: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    likes_count = db.query(models.Like).filter(models.Like.post_id == post.id).count()
    return schemas.Post(
        id=post.id,
        username=post.username,
        content=post.content,
        createdAt=post.created_at,
        updatedAt=post.updated_at,
        likesCount=likes_count
    )


@router.patch(
    "/{postId}",
    response_model=schemas.Post,
    summary="Update a post",
    description="Update the content of an existing post",
    operation_id="updatePost",
    responses={
        400: {
            "description": "Bad request - invalid input or missing required fields",
            "model": schemas.Error
        },
        404: {
            "description": "Resource not found",
            "model": schemas.Error
        },
        500: {
            "description": "Internal server error",
            "model": schemas.Error
        }
    }
)
def update_post(postId: str, post_data: schemas.UpdatePostRequest, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    if not post_data.username or not post_data.content:
        raise HTTPException(status_code=400, detail="Missing required field")
    
    post.content = post_data.content
    from datetime import datetime
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    
    likes_count = db.query(models.Like).filter(models.Like.post_id == post.id).count()
    return schemas.Post(
        id=post.id,
        username=post.username,
        content=post.content,
        createdAt=post.created_at,
        updatedAt=post.updated_at,
        likesCount=likes_count
    )


@router.delete(
    "/{postId}",
    status_code=204,
    summary="Delete a post",
    description="Remove a post that is no longer wanted",
    operation_id="deletePost",
    responses={
        404: {
            "description": "Resource not found",
            "model": schemas.Error
        },
        500: {
            "description": "Internal server error",
            "model": schemas.Error
        }
    }
)
def delete_post(postId: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(post)
    db.commit()
    return None
