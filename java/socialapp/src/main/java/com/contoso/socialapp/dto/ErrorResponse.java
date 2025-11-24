package com.contoso.socialapp.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Error response")
public class ErrorResponse {
    
    @NotNull
    @Schema(description = "Error code or type", example = "BadRequest")
    private String error;
    
    @NotNull
    @Schema(description = "Human-readable error message", example = "Missing required field 'username'")
    private String message;
    
    @Schema(description = "Additional details about the error (optional)", 
            example = "The 'username' field is required but was not provided in the request body")
    private String details;
}
