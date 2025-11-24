package com.contoso.socialapp.repository;

import com.contoso.socialapp.entity.Like;
import com.contoso.socialapp.entity.Post;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface LikeRepository extends JpaRepository<Like, Like.LikeId> {
    
    long countByPostId(String postId);
    
    Optional<Like> findByPostAndUsername(Post post, String username);
}
