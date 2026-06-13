import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Home from "../pages/public/Home";
import ContactUs from "../pages/public/ContactUs";
import Login from "../pages/public/Login";
import Register from "../pages/public/Register";
import Unauthorized from "../pages/public/Unauthorized";
import Properties from "../pages/public/Properties";

import BuyerPage from "../pages/buyer/BuyerPage";
import SellerPage from "../pages/seller/SellerPage";
import AdminPage from "../pages/admin/AdminPage";

import PrivateRoute from "./PrivateRoute";

// main routes component
// public + protected routes yahan handle honge

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* public routes */}

        <Route path="/" element={<Home />} />

        <Route path="/contact" element={<ContactUs />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/unauthorized" element={<Unauthorized />} />
        
        <Route path="/properties" element={<Properties />} />

        {/* protected buyer route */}

        <Route
          path="/buyer"
          element={
            <PrivateRoute allowedRole="buyer">
              <BuyerPage />
            </PrivateRoute>
          }
        />

        {/* protected seller route */}

        <Route
          path="/seller"
          element={
            <PrivateRoute allowedRole="seller">
              <SellerPage />
            </PrivateRoute>
          }
        />

        {/* protected admin route */}

        <Route
          path="/admin"
          element={
            <PrivateRoute allowedRole="admin">
              <AdminPage />
            </PrivateRoute>
          }
        />

        {/* fallback route */}

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
