using System.Text.Json;
using Blazored.LocalStorage;
using Contoso.BlazorApp.Models;

namespace Contoso.BlazorApp.Services;

public class AuthService
{
    private readonly ILocalStorageService _localStorage;
    private UserInfo? _currentUser;
    private const string UserStorageKey = "user";

    public event Action? OnAuthStateChanged;

    public AuthService(ILocalStorageService localStorage)
    {
        _localStorage = localStorage;
    }

    public async Task InitializeAsync()
    {
        try
        {
            var userJson = await _localStorage.GetItemAsStringAsync(UserStorageKey);
            if (!string.IsNullOrEmpty(userJson))
            {
                _currentUser = JsonSerializer.Deserialize<UserInfo>(userJson);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading user information: {ex.Message}");
            await _localStorage.RemoveItemAsync(UserStorageKey);
        }
    }

    public async Task<UserInfo?> GetUserAsync()
    {
        if (_currentUser == null)
        {
            await InitializeAsync();
        }
        return _currentUser;
    }

    public bool IsAuthenticated => _currentUser != null;

    public async Task<UserInfo> LoginAsync(string username)
    {
        var user = new UserInfo { Username = username.Trim() };
        _currentUser = user;
        
        var userJson = JsonSerializer.Serialize(user);
        await _localStorage.SetItemAsStringAsync(UserStorageKey, userJson);
        
        OnAuthStateChanged?.Invoke();
        return user;
    }

    public async Task LogoutAsync()
    {
        _currentUser = null;
        await _localStorage.RemoveItemAsync(UserStorageKey);
        OnAuthStateChanged?.Invoke();
    }
}
