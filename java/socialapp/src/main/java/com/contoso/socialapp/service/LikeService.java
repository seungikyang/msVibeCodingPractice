package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.LikeRequest;
import com.contoso.socialapp.dto.LikeResponse;
import com.contoso.socialapp.entity.Like;
import com.contoso.socialapp.entity.Post;
import com.contoso.socialapp.exception.BadRequestException;
import com.contoso.socialapp.exception.ResourceNotFoundException;
import com.contoso.socialapp.repository.LikeRepository;
import com.contoso.socialapp.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class LikeService {
    
    private final LikeRepository likeRepository;
    private final PostRepository postRepository;
    
    @Transactional
    public LikeResponse likePost(String postId, LikeRequest request) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        if (request.getUsername() == null || request.getUsername().isBlank()) {
            throw new BadRequestException("Missing required field");
        }
        
        // Check if like already exists
        Optional<Like> existingLike = likeRepository.findByPostAndUsername(post, request.getUsername());
        if (existingLike.isPresent()) {
            Like like = existingLike.get();
            return new LikeResponse(
                    like.getPost().getId(),
                    like.getUsername(),
                    like.getCreatedAt()
            );
        }
        
        // Create new like
        Like like = new Like();
        like.setPost(post);
        like.setUsername(request.getUsername());
        like.setCreatedAt(Instant.now());
        
        Like savedLike = likeRepository.save(like);
        return new LikeResponse(
                savedLike.getPost().getId(),
                savedLike.getUsername(),
                savedLike.getCreatedAt()
        );
    }
    
    @Transactional
    public void unlikePost(String postId, String username) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        Like like = likeRepository.findByPostAndUsername(post, username)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        likeRepository.delete(like);
    }
}
