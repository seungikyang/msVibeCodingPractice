package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(name = "NewPostRequest", description = "Request body for creating a new post")
public class CreatePostRequest {
    
    @NotBlank(message = "username is required")
    @Schema(description = "Username of the post author", example = "johndoe")
    private String username;
    
    @NotBlank(message = "content is required")
    @Schema(description = "Content of the post", example = "This is my first post about outdoor activities!")
    private String content;
}
