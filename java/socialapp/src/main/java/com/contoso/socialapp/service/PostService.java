package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.CreatePostRequest;
import com.contoso.socialapp.dto.PostResponse;
import com.contoso.socialapp.dto.UpdatePostRequest;
import com.contoso.socialapp.entity.Post;
import com.contoso.socialapp.exception.BadRequestException;
import com.contoso.socialapp.exception.ResourceNotFoundException;
import com.contoso.socialapp.repository.CommentRepository;
import com.contoso.socialapp.repository.LikeRepository;
import com.contoso.socialapp.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class PostService {
    
    private final PostRepository postRepository;
    private final LikeRepository likeRepository;
    private final CommentRepository commentRepository;
    
    @Transactional(readOnly = true)
    public List<PostResponse> getAllPosts() {
        return postRepository.findAll().stream()
                .map(this::toPostResponse)
                .collect(Collectors.toList());
    }
    
    @Transactional
    public PostResponse createPost(CreatePostRequest request) {
        if (request.getUsername() == null || request.getUsername().isBlank() ||
            request.getContent() == null || request.getContent().isBlank()) {
            throw new BadRequestException("Missing required field");
        }
        
        String postId = UUID.randomUUID().toString();
        Post post = new Post();
        post.setId(postId);
        post.setUsername(request.getUsername());
        post.setContent(request.getContent());
        post.setCreatedAt(Instant.now());
        post.setUpdatedAt(Instant.now());
        
        Post savedPost = postRepository.save(post);
        return toPostResponse(savedPost);
    }
    
    @Transactional(readOnly = true)
    public PostResponse getPost(String postId) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        return toPostResponse(post);
    }
    
    @Transactional
    public PostResponse updatePost(String postId, UpdatePostRequest request) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        if (request.getUsername() == null || request.getUsername().isBlank() ||
            request.getContent() == null || request.getContent().isBlank()) {
            throw new BadRequestException("Missing required field");
        }
        
        post.setContent(request.getContent());
        post.setUpdatedAt(Instant.now());
        
        Post updatedPost = postRepository.save(post);
        return toPostResponse(updatedPost);
    }
    
    @Transactional
    public void deletePost(String postId) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        postRepository.delete(post);
    }
    
    private PostResponse toPostResponse(Post post) {
        int likesCount = (int) likeRepository.countByPostId(post.getId());
        int commentsCount = (int) commentRepository.countByPostId(post.getId());
        return new PostResponse(
                post.getId(),
                post.getUsername(),
                post.getContent(),
                post.getCreatedAt(),
                post.getUpdatedAt(),
                likesCount,
                commentsCount
        );
    }
}
