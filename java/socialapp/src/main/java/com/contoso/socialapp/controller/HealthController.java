package com.contoso.socialapp.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.view.RedirectView;

import java.util.Map;

@RestController
public class HealthController {

    @GetMapping("/")
    public RedirectView root() {
        return new RedirectView("/docs");
    }

    @GetMapping("/api/health")
    public Map<String, String> health() {
        return Map.of(
            "status", "UP",
            "message", "Social App is running successfully!"
        );
    }
}
