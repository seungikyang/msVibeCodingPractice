package com.contoso.socialapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(name = "Post", description = "Post object")
public class PostResponse {
    
    @NotNull
    @Schema(description = "Unique identifier for the post", example = "123e4567-e89b-12d3-a456-426614174000", format = "uuid")
    private String id;
    
    @NotNull
    @Schema(description = "Username of the post author", example = "john_doe")
    private String username;
    
    @NotNull
    @Schema(description = "Content of the post", example = "Just had an amazing hike in the mountains! #outdoorlife")
    private String content;
    
    @NotNull
    @JsonProperty("createdAt")
    @Schema(description = "Timestamp when the post was created", example = "2025-06-01T10:30:00Z")
    private Instant createdAt;
    
    @NotNull
    @JsonProperty("updatedAt")
    @Schema(description = "Timestamp when the post was last updated", example = "2025-06-01T10:30:00Z")
    private Instant updatedAt;
    
    @NotNull
    @Min(0)
    @JsonProperty("likesCount")
    @Schema(description = "Number of likes on the post", example = "15")
    private Integer likesCount;
    
    @NotNull
    @Min(0)
    @JsonProperty("commentsCount")
    @Schema(description = "Number of comments on the post", example = "3")
    private Integer commentsCount;
}
