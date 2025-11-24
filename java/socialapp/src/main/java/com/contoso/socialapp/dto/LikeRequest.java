package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Request to like a post")
public class LikeRequest {
    
    @NotBlank(message = "username is required")
    @Schema(description = "Username of the user who wants to like the post", example = "bobsmith")
    private String username;
}
