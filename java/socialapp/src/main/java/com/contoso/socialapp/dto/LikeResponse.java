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
@Schema(name = "LikeResponse", description = "Like response object")
public class LikeResponse {
    
    @NotNull
    @JsonProperty("postId")
    @Schema(description = "ID of the liked post", example = "123e4567-e89b-12d3-a456-426614174000", format = "uuid")
    private String postId;
    
    @NotNull
    @Schema(description = "Username who liked the post", example = "mike_wilson")
    private String username;
    
    @NotNull
    @JsonProperty("likedAt")
    @Schema(description = "Timestamp when the post was liked", example = "2025-06-01T12:00:00Z")
    private Instant likedAt;
}
