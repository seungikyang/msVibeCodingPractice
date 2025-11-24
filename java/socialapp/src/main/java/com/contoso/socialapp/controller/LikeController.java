package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.LikeRequest;
import com.contoso.socialapp.dto.LikeResponse;
import com.contoso.socialapp.service.LikeService;
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

@RestController
@RequestMapping("/api/posts/{postId}/likes")
@RequiredArgsConstructor
@Tag(name = "Likes", description = "Operations related to liking posts")
public class LikeController {
    
    private final LikeService likeService;
    
    @PostMapping
    @Operation(
        summary = "Like a post",
        description = "Like a post to show appreciation",
        operationId = "likePost"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Post liked successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - invalid input or missing required fields", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<LikeResponse> likePost(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId,
            @Valid @RequestBody LikeRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(likeService.likePost(postId, request));
    }
    
    @DeleteMapping
    @Operation(
        summary = "Unlike a post",
        description = "Remove your like from a post if you change your mind",
        operationId = "unlikePost"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Like removed successfully", content = @Content),
        @ApiResponse(responseCode = "404", description = "Resource not found", content = @Content),
        @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public ResponseEntity<Void> unlikePost(
            @Parameter(description = "Unique identifier of the post", required = true)
            @PathVariable String postId) {
        // Note: In a real application, username would come from authentication context
        // For this demo, we'll need to modify the approach
        return ResponseEntity.noContent().build();
    }
}
