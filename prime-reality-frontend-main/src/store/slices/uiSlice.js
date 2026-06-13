import { createSlice } from "@reduxjs/toolkit";

// UI state
// modal/sidebar/loading jaise UI states yahan manage honge

const initialState = {
  isModalOpen: false,
  isSidebarOpen: false,
  globalLoading: false,
};

const uiSlice = createSlice({
  name: "ui",

  initialState,

  reducers: {
    openModal: (state) => {
      state.isModalOpen = true;
    },

    closeModal: (state) => {
      state.isModalOpen = false;
    },

    toggleSidebar: (state) => {
      state.isSidebarOpen = !state.isSidebarOpen;
    },

    setGlobalLoading: (state, action) => {
      state.globalLoading = action.payload;
    },
  },
});

export const {
  openModal,
  closeModal,
  toggleSidebar,
  setGlobalLoading,
} = uiSlice.actions;

export default uiSlice.reducer;