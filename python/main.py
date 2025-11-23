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

# Include routers WITH /api prefix for frontend compatibility
app.include_router(posts.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(likes.router, prefix="/api")


def custom_openapi():
    """Customize OpenAPI schema to match openapi.yaml"""
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.0.1",  # Force 3.0.1 instead of FastAPI default 3.1.0
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
    
    # Remove the root "/" endpoint from paths
    if "paths" in openapi_schema and "/" in openapi_schema["paths"]:
        del openapi_schema["paths"]["/"]
    
    # Convert path parameters to use $ref
    # And convert error responses to use $ref instead of inline schemas
    # And update response descriptions to match openapi.yaml
    if "paths" in openapi_schema:
        response_descriptions = {
            "/posts": {
                "get": {"200": "Successfully retrieved list of posts"},
                "post": {"201": "Post created successfully"}
            },
            "/posts/{postId}": {
                "get": {"200": "Successfully retrieved post"},
                "patch": {"200": "Post updated successfully"},
                "delete": {"204": "Post deleted successfully"}
            },
            "/posts/{postId}/comments": {
                "get": {"200": "Successfully retrieved list of comments"},
                "post": {"201": "Comment created successfully"}
            },
            "/posts/{postId}/comments/{commentId}": {
                "get": {"200": "Successfully retrieved comment"},
                "patch": {"200": "Comment updated successfully"},
                "delete": {"204": "Comment deleted successfully"}
            },
            "/posts/{postId}/likes": {
                "post": {"201": "Post liked successfully"},
                "delete": {"204": "Post unliked successfully"}
            }
        }
        
        for path, methods in openapi_schema["paths"].items():
            for method, operation in methods.items():
                # Convert path parameters to use $ref
                if "parameters" in operation:
                    new_parameters = []
                    for param in operation["parameters"]:
                        if param.get("in") == "path":
                            if param.get("name") == "postId":
                                new_parameters.append({"$ref": "#/components/parameters/PostId"})
                            elif param.get("name") == "commentId":
                                new_parameters.append({"$ref": "#/components/parameters/CommentId"})
                            else:
                                new_parameters.append(param)
                        elif param.get("in") == "query":
                            # Keep query parameters as-is but remove extra fields
                            clean_param = {
                                "name": param.get("name"),
                                "in": "query",
                                "required": param.get("required", False),
                                "schema": {"type": param.get("schema", {}).get("type", "string")}
                            }
                            if "description" in param:
                                clean_param["description"] = param["description"]
                            new_parameters.append(clean_param)
                        else:
                            new_parameters.append(param)
                    operation["parameters"] = new_parameters
                
                if "responses" in operation:
                    # Update descriptions
                    if path in response_descriptions and method in response_descriptions[path]:
                        for status_code, description in response_descriptions[path][method].items():
                            if status_code in operation["responses"]:
                                operation["responses"][status_code]["description"] = description
                    
                    # Remove title from response schemas
                    for status_code, response in operation["responses"].items():
                        if "content" in response and "application/json" in response["content"]:
                            if "schema" in response["content"]["application/json"]:
                                response["content"]["application/json"]["schema"].pop("title", None)
                    
                    # Replace 400, 404, 500 responses with $ref
                    if "400" in operation["responses"]:
                        operation["responses"]["400"] = {"$ref": "#/components/responses/BadRequest"}
                    if "404" in operation["responses"]:
                        operation["responses"]["404"] = {"$ref": "#/components/responses/NotFound"}
                    if "500" in operation["responses"]:
                        operation["responses"]["500"] = {"$ref": "#/components/responses/InternalServerError"}
                    
                    # Remove 422 validation error responses
                    if "422" in operation["responses"]:
                        del operation["responses"]["422"]
    
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
