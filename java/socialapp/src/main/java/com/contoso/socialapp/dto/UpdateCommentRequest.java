package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Request to update a comment")
public class UpdateCommentRequest {
    
    @NotBlank(message = "username is required")
    @Schema(description = "Username of the comment author (for verification)", example = "janedoe")
    private String username;
    
    @NotBlank(message = "content is required")
    @Schema(description = "Updated content of the comment", example = "Great post! I really love outdoor activities.")
    private String content;
}
