from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/posts/{postId}/likes", tags=["Likes"])


@router.post(
    "",
    response_model=schemas.Like,
    status_code=201,
    summary="Like a post",
    description="Express appreciation by liking a post",
    operation_id="likePost",
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
def like_post(postId: str, like_data: schemas.LikeRequest, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    if not like_data.username:
        raise HTTPException(status_code=400, detail="Missing required field")
    
    existing_like = db.query(models.Like).filter(
        models.Like.post_id == postId,
        models.Like.username == like_data.username
    ).first()
    
    if existing_like:
        return schemas.Like(
            postId=existing_like.post_id,
            username=existing_like.username,
            createdAt=existing_like.created_at
        )
    
    new_like = models.Like(
        post_id=postId,
        username=like_data.username
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return schemas.Like(
        postId=new_like.post_id,
        username=new_like.username,
        createdAt=new_like.created_at
    )


@router.delete(
    "",
    status_code=204,
    summary="Unlike a post",
    description="Remove a like from a post",
    operation_id="unlikePost",
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
def unlike_post(
    postId: str,
    username: str = Query(..., description="Username of the user who wants to unlike the post"),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    if not post:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    like = db.query(models.Like).filter(
        models.Like.post_id == postId,
        models.Like.username == username
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(like)
    db.commit()
    return None
