import { createSlice } from "@reduxjs/toolkit";

// property state
// listing/search/filter data future me yahan manage hoga

const initialState = {
  properties: [],
  selectedProperty: null,
  filters: {
    location: "",
    type: "",
    bedrooms: "",
    maxPrice: "",
  },
  loading: false,
  error: null,
};

const propertySlice = createSlice({
  name: "property",

  initialState,

  reducers: {
    setProperties: (state, action) => {
      state.properties = action.payload;
    },

    setSelectedProperty: (state, action) => {
      state.selectedProperty = action.payload;
    },

    setFilters: (state, action) => {
      state.filters = {
        ...state.filters,
        ...action.payload,
      };
    },

    clearFilters: (state) => {
      state.filters = initialState.filters;
    },
  },
});

export const {
  setProperties,
  setSelectedProperty,
  setFilters,
  clearFilters,
} = propertySlice.actions;

export default propertySlice.reducer;