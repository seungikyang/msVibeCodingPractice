package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Request to update a post")
public class UpdatePostRequest {
    
    @NotBlank(message = "username is required")
    @Schema(description = "Username of the post author (for verification)", example = "johndoe")
    private String username;
    
    @NotBlank(message = "content is required")
    @Schema(description = "Updated content of the post", example = "This is my updated post about outdoor activities!")
    private String content;
}
