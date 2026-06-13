import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./slices/authSlice";
import propertyReducer from "./slices/propertySlice";
import uiReducer from "./slices/uiSlice";

// redux store
// global states yahan register honge

const store = configureStore({
  reducer: {
    auth: authReducer,
    property: propertyReducer,
    ui: uiReducer,
  },
});

export default store;