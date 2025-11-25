namespace Contoso.BlazorApp.Models;

public class Post
{
    public string Id { get; set; } = string.Empty;
    public string Username { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    public int LikesCount { get; set; }
    public int CommentsCount { get; set; }
    public bool IsLiked { get; set; }
}

public class Comment
{
    public string Id { get; set; } = string.Empty;
    public string PostId { get; set; } = string.Empty;
    public string Username { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public class CreatePostRequest
{
    public string Username { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
}

public class UpdatePostRequest
{
    public string Username { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
}

public class CreateCommentRequest
{
    public string Username { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
}

public class UpdateCommentRequest
{
    public string Username { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
}

public class LikeRequest
{
    public string Username { get; set; } = string.Empty;
}

public class LikeResponse
{
    public int LikesCount { get; set; }
}

public class UserInfo
{
    public string Username { get; set; } = string.Empty;
}
