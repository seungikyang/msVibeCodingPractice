package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(name = "NewCommentRequest", description = "Request body for creating a new comment")
public class CreateCommentRequest {
    
    @NotBlank(message = "username is required")
    @Schema(description = "Username of the comment author", example = "janedoe")
    private String username;
    
    @NotBlank(message = "content is required")
    @Schema(description = "Content of the comment", example = "Great post! I love outdoor activities too.")
    private String content;
}
