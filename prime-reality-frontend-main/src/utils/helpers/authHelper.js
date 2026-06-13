// auth helper functions
// token aur role ka duplicate code avoid karne ke liye

export const saveAuthTokens = (accessToken, refreshToken) => {
  localStorage.setItem("access_token", accessToken);
  localStorage.setItem("refresh_token", refreshToken);
};

export const saveUserRole = (role) => {
  localStorage.setItem("role", role);
};

export const getAccessToken = () => {
  return localStorage.getItem("access_token");
};

export const getRefreshToken = () => {
  return localStorage.getItem("refresh_token");
};

export const getUserRole = () => {
  return localStorage.getItem("role");
};

export const clearAuthData = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("role");
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};