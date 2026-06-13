import { createSlice } from "@reduxjs/toolkit";

// auth initial state
// token aur role localStorage se read kar rahe hain

const initialState = {
  accessToken: localStorage.getItem("access_token") || null,
  refreshToken: localStorage.getItem("refresh_token") || null,
  role: localStorage.getItem("role") || null,
  user: null,
  isAuthenticated: !!localStorage.getItem("access_token"),
};

const authSlice = createSlice({
  name: "auth",

  initialState,

  reducers: {
    loginSuccess: (state, action) => {
      state.accessToken = action.payload.accessToken;
      state.refreshToken = action.payload.refreshToken;
      state.role = action.payload.role;
      state.user = action.payload.user;
      state.isAuthenticated = true;
    },

    setUser: (state, action) => {
      state.user = action.payload;
      state.role = action.payload.role;
    },

    logout: (state) => {
      state.accessToken = null;
      state.refreshToken = null;
      state.role = null;
      state.user = null;
      state.isAuthenticated = false;

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("role");
    },
  },
});

export const {
  loginSuccess,
  setUser,
  logout,
} = authSlice.actions;

export default authSlice.reducer;