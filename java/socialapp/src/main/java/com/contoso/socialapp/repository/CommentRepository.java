package com.contoso.socialapp.repository;

import com.contoso.socialapp.entity.Comment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CommentRepository extends JpaRepository<Comment, String> {
    
    List<Comment> findByPostId(String postId);
    
    Optional<Comment> findByIdAndPostId(String id, String postId);
    
    long countByPostId(String postId);
}
