package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.CommentResponse;
import com.contoso.socialapp.dto.CreateCommentRequest;
import com.contoso.socialapp.dto.UpdateCommentRequest;
import com.contoso.socialapp.service.CommentService;
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
@RequestMapping("/api/posts/{postId}/comments")
@RequiredArgsConstructor
@Tag(name = "Comments", description = "Operations related to comments on posts")
public class CommentController {
    
    private final CommentService commentService;
    
    @GetMapping
    @Operation(
        summary = "List comments for a post",
        description = "Retrieve all comments on a specific post",
        operationId = "getCommentsByPostId"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved list of comments"),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<List<CommentResponse>> listComments(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId) {
        return ResponseEntity.ok(commentService.getCommentsByPost(postId));
    }
    
    @PostMapping
    @Operation(
        summary = "Create a comment",
        description = "Add a comment to a post to share your thoughts",
        operationId = "createComment"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Comment created successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - invalid input or missing required fields", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<CommentResponse> createComment(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId,
            @Valid @RequestBody CreateCommentRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(commentService.createComment(postId, request));
    }
    
    @GetMapping("/{commentId}")
    @Operation(
        summary = "Get a specific comment",
        description = "Retrieve a specific comment by its ID",
        operationId = "getCommentById"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved comment"),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<CommentResponse> getComment(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId,
            @Parameter(description = "Unique identifier of the comment", required = true)
            @PathVariable String commentId) {
        return ResponseEntity.ok(commentService.getComment(postId, commentId));
    }
    
    @PatchMapping("/{commentId}")
    @Operation(
        summary = "Update a comment",
        description = "Update an existing comment to correct or revise it",
        operationId = "updateComment"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Comment updated successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - invalid input or missing required fields", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<CommentResponse> updateComment(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId,
            @Parameter(description = "Unique identifier of the comment", required = true)
            @PathVariable String commentId,
            @Valid @RequestBody UpdateCommentRequest request) {
        return ResponseEntity.ok(commentService.updateComment(postId, commentId, request));
    }
    
    @DeleteMapping("/{commentId}")
    @Operation(
        summary = "Delete a comment",
        description = "Delete a comment if necessary",
        operationId = "deleteComment"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Comment deleted successfully", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<Void> deleteComment(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId,
            @Parameter(description = "Unique identifier of the comment", required = true)
            @PathVariable String commentId) {
        commentService.deleteComment(postId, commentId);
        return ResponseEntity.noContent().build();
    }
}
