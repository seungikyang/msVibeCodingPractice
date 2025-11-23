from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import posts, comments, likes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on application startup"""
    init_db()
    yield


# Initialize FastAPI with metadata matching openapi.yaml
app = FastAPI(
    title="Simple Social Media API",
    description=(
        "A basic social networking service API that allows users to create, read, update, and delete posts,\n"
        "add comments, and like/unlike posts. This API supports web and mobile frontend applications.\n"
    ),
    version="1.0.0",
    contact={"name": "Contoso Product Owner / Tech Lead"},
    openapi_version="3.0.1",
    openapi_tags=[
        {
            "name": "Posts",
            "description": "Operations related to posts management"
        },
        {
            "name": "Comments",
            "description": "Operations related to comments on posts"
        },
        {
            "name": "Likes",
            "description": "Operations related to liking posts"
        }
    ],
    servers=[
        {
            "url": "http://localhost:8080/api",
            "description": "Local development server"
        }
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers WITHOUT /api prefix (since it's in servers.url)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)


def custom_openapi():
    """Customize OpenAPI schema to match openapi.yaml"""
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
        servers=app.servers,
        tags=[
            {"name": "Posts", "description": "Operations related to posts management"},
            {"name": "Comments", "description": "Operations related to comments on posts"},
            {"name": "Likes", "description": "Operations related to liking posts"}
        ]
    )
    
    # Add contact info
    if "info" not in openapi_schema:
        openapi_schema["info"] = {}
    openapi_schema["info"]["contact"] = {"name": "Contoso Product Owner / Tech Lead"}
    
    # Remove HTTPValidationError and ValidationError schemas
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        schemas_to_remove = ["HTTPValidationError", "ValidationError"]
        for schema_name in schemas_to_remove:
            openapi_schema["components"]["schemas"].pop(schema_name, None)
    
    # Fix Error schema details field - change anyOf to type: string
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        if "Error" in openapi_schema["components"]["schemas"]:
            error_schema = openapi_schema["components"]["schemas"]["Error"]
            if "properties" in error_schema and "details" in error_schema["properties"]:
                error_schema["properties"]["details"] = {
                    "type": "string",
                    "description": "Additional details about the error (optional)",
                    "example": "The 'username' field is required but was not provided in the request body"
                }
    
    # Remove title fields from all schema properties
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        for schema_name, schema in openapi_schema["components"]["schemas"].items():
            # Remove title from schema itself
            schema.pop("title", None)
            
            # Remove title from properties
            if "properties" in schema:
                for prop_name, prop in schema["properties"].items():
                    prop.pop("title", None)
                    
                    # Convert examples array to single example if it exists
                    if "examples" in prop and isinstance(prop["examples"], list) and len(prop["examples"]) > 0:
                        prop["example"] = prop["examples"][0]
                        del prop["examples"]
    
    # Add components.parameters matching openapi.yaml
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    openapi_schema["components"]["parameters"] = {
        "PostId": {
            "name": "postId",
            "in": "path",
            "description": "Unique identifier of the post",
            "required": True,
            "schema": {"type": "string"}
        },
        "CommentId": {
            "name": "commentId",
            "in": "path",
            "description": "Unique identifier of the comment",
            "required": True,
            "schema": {"type": "string"}
        }
    }
    
    # Add components.responses matching openapi.yaml
    openapi_schema["components"]["responses"] = {
        "BadRequest": {
            "description": "Bad request - invalid input or missing required fields",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"},
                    "example": {
                        "error": "BadRequest",
                        "message": "Invalid input data",
                        "details": "The 'content' field cannot be empty"
                    }
                }
            }
        },
        "NotFound": {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"},
                    "example": {
                        "error": "NotFound",
                        "message": "Resource not found",
                        "details": "Post with id 'post-123' does not exist"
                    }
                }
            }
        },
        "InternalServerError": {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"},
                    "example": {
                        "error": "InternalServerError",
                        "message": "An unexpected error occurred",
                        "details": "Please try again later or contact support"
                    }
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    """Root endpoint redirects to Swagger UI"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
