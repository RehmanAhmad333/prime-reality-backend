import { Navigate } from "react-router-dom";

import {
  getAccessToken,
  getUserRole,
} from "../utils/helpers/authHelper";

// protected route
// token aur role validation yahan handle ho rahi hai

function PrivateRoute({ children, allowedRole }) {
  const token = getAccessToken();

  const role = getUserRole();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  const normalizedAllowedRole = allowedRole?.toString().toLowerCase();

  const normalizedRole = role?.toString().toLowerCase();

  if (normalizedAllowedRole && normalizedRole !== normalizedAllowedRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}

export default PrivateRoute;