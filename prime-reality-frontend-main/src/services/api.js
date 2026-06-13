import axios from "axios";

import {
  getAccessToken,
  getRefreshToken,
  saveAuthTokens,
  clearAuthData,
} from "../utils/helpers/authHelper";

// axios instance
// base URL .env se aa raha hai
// timeout is liye add kiya hai taake request forever pending na rahe

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 20000,
  headers: {
    "Content-Type": "application/json",
  },
});

// request interceptor
// protected APIs ke sath access token auto send hoga

api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },

  (error) => Promise.reject(error)
);

// response interceptor
// access token expire ho jaye to refresh token se new token lene ki try hogi

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = getRefreshToken();

        if (!refreshToken) {
          clearAuthData();
          window.location.href = "/login";

          return Promise.reject(error);
        }

        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/auth/refresh`,
          {},
          {
            timeout: 20000,
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          }
        );

        const newAccessToken = response.data.access_token;

        saveAuthTokens(newAccessToken, refreshToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        clearAuthData();
        window.location.href = "/login";

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;