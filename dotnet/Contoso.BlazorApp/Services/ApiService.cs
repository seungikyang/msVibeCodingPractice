using System.Net.Http.Json;
using System.Text.Json;
using Contoso.BlazorApp.Models;

namespace Contoso.BlazorApp.Services;

public class ApiService
{
    private readonly HttpClient _httpClient;
    private readonly AuthService _authService;
    private readonly JsonSerializerOptions _jsonOptions;

    public ApiService(HttpClient httpClient, AuthService authService)
    {
        _httpClient = httpClient;
        _authService = authService;
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
    }

    private async Task<HttpRequestMessage> CreateRequestAsync(HttpMethod method, string url)
    {
        var request = new HttpRequestMessage(method, url);
        var user = await _authService.GetUserAsync();
        
        if (user != null && !string.IsNullOrEmpty(user.Username))
        {
            request.Headers.Add("x-username", Uri.EscapeDataString(user.Username));
        }
        
        return request;
    }

    // Post APIs
    public async Task<List<Post>> GetPostsAsync()
    {
        var request = await CreateRequestAsync(HttpMethod.Get, "/api/posts");
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<List<Post>>(_jsonOptions) ?? new List<Post>();
    }

    public async Task<Post?> GetPostAsync(string postId)
    {
        var request = await CreateRequestAsync(HttpMethod.Get, $"/api/posts/{postId}");
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<Post>(_jsonOptions);
    }

    public async Task<Post?> CreatePostAsync(string content, string username)
    {
        var request = await CreateRequestAsync(HttpMethod.Post, "/api/posts");
        request.Content = JsonContent.Create(new CreatePostRequest
        {
            Username = username,
            Content = content
        });
        
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<Post>(_jsonOptions);
    }

    public async Task<Post?> UpdatePostAsync(string postId, string content, string username)
    {
        var request = await CreateRequestAsync(new HttpMethod("PATCH"), $"/api/posts/{postId}");
        request.Content = JsonContent.Create(new UpdatePostRequest
        {
            Username = username,
            Content = content
        });
        
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<Post>(_jsonOptions);
    }

    public async Task DeletePostAsync(string postId)
    {
        var request = await CreateRequestAsync(HttpMethod.Delete, $"/api/posts/{postId}");
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
    }

    // Like APIs
    public async Task<LikeResponse?> LikePostAsync(string postId, string username)
    {
        var request = await CreateRequestAsync(HttpMethod.Post, $"/api/posts/{postId}/likes");
        request.Content = JsonContent.Create(new LikeRequest { Username = username });
        
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<LikeResponse>(_jsonOptions);
    }

    public async Task UnlikePostAsync(string postId)
    {
        var request = await CreateRequestAsync(HttpMethod.Delete, $"/api/posts/{postId}/likes");
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        // Unlike returns 204 No Content, so don't try to parse JSON
    }

    // Comment APIs
    public async Task<List<Comment>> GetCommentsAsync(string postId)
    {
        var request = await CreateRequestAsync(HttpMethod.Get, $"/api/posts/{postId}/comments");
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<List<Comment>>(_jsonOptions) ?? new List<Comment>();
    }

    public async Task<Comment?> CreateCommentAsync(string postId, string content, string username)
    {
        var request = await CreateRequestAsync(HttpMethod.Post, $"/api/posts/{postId}/comments");
        request.Content = JsonContent.Create(new CreateCommentRequest
        {
            Username = username,
            Content = content
        });
        
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<Comment>(_jsonOptions);
    }

    public async Task<Comment?> UpdateCommentAsync(string postId, string commentId, string content, string username)
    {
        var request = await CreateRequestAsync(new HttpMethod("PATCH"), $"/api/posts/{postId}/comments/{commentId}");
        request.Content = JsonContent.Create(new UpdateCommentRequest
        {
            Username = username,
            Content = content
        });
        
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
        
        return await response.Content.ReadFromJsonAsync<Comment>(_jsonOptions);
    }

    public async Task DeleteCommentAsync(string postId, string commentId)
    {
        var request = await CreateRequestAsync(HttpMethod.Delete, $"/api/posts/{postId}/comments/{commentId}");
        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();
    }
}
