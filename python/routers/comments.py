import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/posts/{postId}/comments", tags=["Comments"])


@router.get(
    "",
    response_model=list[schemas.Comment],
    summary="Get all comments for a post",
    description="Retrieve all comments associated with a specific post",
    operation_id="listComments",
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
def list_comments(postId: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    comments = db.query(models.Comment).filter(models.Comment.post_id == postId).all()
    result = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "postId": comment.post_id,
            "username": comment.username,
            "content": comment.content,
            "createdAt": comment.created_at,
            "updatedAt": comment.updated_at
        }
        result.append(schemas.Comment(**comment_dict))
    return result


@router.post(
    "",
    response_model=schemas.Comment,
    status_code=201,
    summary="Create a comment",
    description="Add a new comment to a specific post",
    operation_id="createComment",
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
def create_comment(postId: str, comment_data: schemas.CreateCommentRequest, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    if not comment_data.username or not comment_data.content:
        raise HTTPException(status_code=400, detail="Missing required field")
    
    comment_id = f"comment-{uuid.uuid4().hex[:8]}"
    new_comment = models.Comment(
        id=comment_id,
        post_id=postId,
        username=comment_data.username,
        content=comment_data.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return schemas.Comment(
        id=new_comment.id,
        postId=new_comment.post_id,
        username=new_comment.username,
        content=new_comment.content,
        createdAt=new_comment.created_at,
        updatedAt=new_comment.updated_at
    )


@router.get(
    "/{commentId}",
    response_model=schemas.Comment,
    summary="Get a specific comment",
    description="Retrieve details of a specific comment",
    operation_id="getComment",
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
def get_comment(postId: str, commentId: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    comment = db.query(models.Comment).filter(
        models.Comment.id == commentId,
        models.Comment.post_id == postId
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return schemas.Comment(
        id=comment.id,
        postId=comment.post_id,
        username=comment.username,
        content=comment.content,
        createdAt=comment.created_at,
        updatedAt=comment.updated_at
    )


@router.patch(
    "/{commentId}",
    response_model=schemas.Comment,
    summary="Update a comment",
    description="Modify or revise an existing comment",
    operation_id="updateComment",
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
def update_comment(postId: str, commentId: str, comment_data: schemas.UpdateCommentRequest, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    comment = db.query(models.Comment).filter(
        models.Comment.id == commentId,
        models.Comment.post_id == postId
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    if not comment_data.username or not comment_data.content:
        raise HTTPException(status_code=400, detail="Missing required field")
    
    comment.content = comment_data.content
    from datetime import datetime
    comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(comment)
    
    return schemas.Comment(
        id=comment.id,
        postId=comment.post_id,
        username=comment.username,
        content=comment.content,
        createdAt=comment.created_at,
        updatedAt=comment.updated_at
    )


@router.delete(
    "/{commentId}",
    status_code=204,
    summary="Delete a comment",
    description="Remove a comment from a post",
    operation_id="deleteComment",
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
def delete_comment(postId: str, commentId: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    comment = db.query(models.Comment).filter(
        models.Comment.id == commentId,
        models.Comment.post_id == postId
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(comment)
    db.commit()
    return None
