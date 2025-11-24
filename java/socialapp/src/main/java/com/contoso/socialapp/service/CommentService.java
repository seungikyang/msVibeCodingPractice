package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.CommentResponse;
import com.contoso.socialapp.dto.CreateCommentRequest;
import com.contoso.socialapp.dto.UpdateCommentRequest;
import com.contoso.socialapp.entity.Comment;
import com.contoso.socialapp.entity.Post;
import com.contoso.socialapp.exception.BadRequestException;
import com.contoso.socialapp.exception.ResourceNotFoundException;
import com.contoso.socialapp.repository.CommentRepository;
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
public class CommentService {
    
    private final CommentRepository commentRepository;
    private final PostRepository postRepository;
    
    @Transactional(readOnly = true)
    public List<CommentResponse> getCommentsByPost(String postId) {
        postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        return commentRepository.findByPostId(postId).stream()
                .map(this::toCommentResponse)
                .collect(Collectors.toList());
    }
    
    @Transactional
    public CommentResponse createComment(String postId, CreateCommentRequest request) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        if (request.getUsername() == null || request.getUsername().isBlank() ||
            request.getContent() == null || request.getContent().isBlank()) {
            throw new BadRequestException("Missing required field");
        }
        
        String commentId = UUID.randomUUID().toString();
        Comment comment = new Comment();
        comment.setId(commentId);
        comment.setPost(post);
        comment.setUsername(request.getUsername());
        comment.setContent(request.getContent());
        comment.setCreatedAt(Instant.now());
        comment.setUpdatedAt(Instant.now());
        
        Comment savedComment = commentRepository.save(comment);
        return toCommentResponse(savedComment);
    }
    
    @Transactional(readOnly = true)
    public CommentResponse getComment(String postId, String commentId) {
        postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        Comment comment = commentRepository.findByIdAndPostId(commentId, postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        return toCommentResponse(comment);
    }
    
    @Transactional
    public CommentResponse updateComment(String postId, String commentId, UpdateCommentRequest request) {
        postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        Comment comment = commentRepository.findByIdAndPostId(commentId, postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        if (request.getUsername() == null || request.getUsername().isBlank() ||
            request.getContent() == null || request.getContent().isBlank()) {
            throw new BadRequestException("Missing required field");
        }
        
        comment.setContent(request.getContent());
        comment.setUpdatedAt(Instant.now());
        
        Comment updatedComment = commentRepository.save(comment);
        return toCommentResponse(updatedComment);
    }
    
    @Transactional
    public void deleteComment(String postId, String commentId) {
        postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        Comment comment = commentRepository.findByIdAndPostId(commentId, postId)
                .orElseThrow(() -> new ResourceNotFoundException("Resource not found"));
        
        commentRepository.delete(comment);
    }
    
    private CommentResponse toCommentResponse(Comment comment) {
        return new CommentResponse(
                comment.getId(),
                comment.getPost().getId(),
                comment.getUsername(),
                comment.getContent(),
                comment.getCreatedAt(),
                comment.getUpdatedAt()
        );
    }
}
