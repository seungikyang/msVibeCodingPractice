package com.contoso.socialapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(name = "Comment", description = "Comment object")
public class CommentResponse {
    
    @NotNull
    @Schema(description = "Unique identifier for the comment", example = "987fcdeb-51a2-43d1-9f6b-123456789abc", format = "uuid")
    private String id;
    
    @NotNull
    @JsonProperty("postId")
    @Schema(description = "ID of the post this comment belongs to", example = "123e4567-e89b-12d3-a456-426614174000", format = "uuid")
    private String postId;
    
    @NotNull
    @Schema(description = "Username of the comment author", example = "jane_smith")
    private String username;
    
    @NotNull
    @Schema(description = "Content of the comment", example = "Great photo! Where was this taken?")
    private String content;
    
    @NotNull
    @JsonProperty("createdAt")
    @Schema(description = "Timestamp when the comment was created", example = "2025-06-01T11:15:00Z")
    private Instant createdAt;
    
    @NotNull
    @JsonProperty("updatedAt")
    @Schema(description = "Timestamp when the comment was last updated", example = "2025-06-01T11:15:00Z")
    private Instant updatedAt;
}
