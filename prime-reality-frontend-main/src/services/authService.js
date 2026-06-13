import api from "./api";

// auth APIs
// login, register aur user profile yahan handle honge

export const registerUser = async (userData) => {
  const response = await api.post(
    "/auth/register",
    userData
  );

  return response.data;
};

export const loginUser = async (userData) => {
  const response = await api.post(
    "/auth/login",
    userData
  );

  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/users/me");

  return response.data;
};

export const updateCurrentUser = async (userData) => {
  const response = await api.put(
    "/users/me",
    userData
  );

  return response.data;
};

// backend logout endpoint nahi hai
// logout client side pe localStorage clear karke hoga

export const logoutUser = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("role");
};