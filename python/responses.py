"""Common HTTP response models for the API"""

from fastapi import status
from fastapi.responses import JSONResponse
from schemas import Error


def bad_request_response():
    """Bad request - invalid input or missing required fields"""
    return {
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request - invalid input or missing required fields",
            "content": {
                "application/json": {
                    "schema": Error.model_json_schema(),
                    "example": {
                        "error": "BadRequest",
                        "message": "Invalid input data",
                        "details": "The 'content' field cannot be empty"
                    }
                }
            }
        }
    }


def not_found_response():
    """Resource not found"""
    return {
        status.HTTP_404_NOT_FOUND: {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "schema": Error.model_json_schema(),
                    "example": {
                        "error": "NotFound",
                        "message": "Resource not found",
                        "details": "Post with id 'post-123' does not exist"
                    }
                }
            }
        }
    }


def internal_server_error_response():
    """Internal server error"""
    return {
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "schema": Error.model_json_schema(),
                    "example": {
                        "error": "InternalServerError",
                        "message": "An unexpected error occurred",
                        "details": "Please try again later or contact support"
                    }
                }
            }
        }
    }


def get_common_responses():
    """Get common responses for all endpoints"""
    responses = {}
    responses.update(bad_request_response())
    responses.update(not_found_response())
    responses.update(internal_server_error_response())
    return responses
