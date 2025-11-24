package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.CreatePostRequest;
import com.contoso.socialapp.dto.PostResponse;
import com.contoso.socialapp.dto.UpdatePostRequest;
import com.contoso.socialapp.service.PostService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/posts")
@RequiredArgsConstructor
@Tag(name = "Posts", description = "Operations related to posts management")
public class PostController {
    
    private final PostService postService;
    
    @GetMapping
    @Operation(
        summary = "List all posts",
        description = "Retrieve all recent posts to browse what others are sharing",
        operationId = "getPosts"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved list of posts"),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<List<PostResponse>> listPosts() {
        return ResponseEntity.ok(postService.getAllPosts());
    }
    
    @PostMapping
    @Operation(
        summary = "Create a new post",
        description = "Create a new post to share something with others",
        operationId = "createPost"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Post created successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - invalid input or missing required fields", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<PostResponse> createPost(@Valid @RequestBody CreatePostRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(postService.createPost(request));
    }
    
    @GetMapping("/{postId}")
    @Operation(
        summary = "Get a specific post",
        description = "Retrieve a specific post by its ID to read in detail",
        operationId = "getPostById"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved post"),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<PostResponse> getPost(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId) {
        return ResponseEntity.ok(postService.getPost(postId));
    }
    
    @PatchMapping("/{postId}")
    @Operation(
        summary = "Update a post",
        description = "Update an existing post if you made a mistake or have something to add",
        operationId = "updatePost"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Post updated successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - invalid input or missing required fields", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<PostResponse> updatePost(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId,
            @Valid @RequestBody UpdatePostRequest request) {
        return ResponseEntity.ok(postService.updatePost(postId, request));
    }
    
    @DeleteMapping("/{postId}")
    @Operation(
        summary = "Delete a post",
        description = "Delete a post if you no longer want it shared",
        operationId = "deletePost"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Post deleted successfully", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<Void> deletePost(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId) {
        postService.deletePost(postId);
        return ResponseEntity.noContent().build();
    }
}
