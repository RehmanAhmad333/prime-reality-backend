import { useState } from "react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import { useDispatch } from "react-redux";

import {
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";

import Navbar from "../../components/common/Navbar";
import Footer from "../../components/common/Footer";

import {
  registerUser,
  getCurrentUser,
} from "../../services/authService";

import {
  saveAuthTokens,
  saveUserRole,
} from "../../utils/helpers/authHelper";

import {
  validateEmail,
  validatePassword,
} from "../../utils/validators/authValidator";

import { loginSuccess } from "../../store/slices/authSlice";

// register page
// strong password validation rakhi hai
// password visibility professional icon se handle ho rahi hai

function Register() {
  const navigate = useNavigate();

  const dispatch = useDispatch();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone: "",
    role: "buyer",
    password: "",
    confirm_password: "",
  });

  const [showPassword, setShowPassword] = useState(false);

  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    if (error) {
      setError("");
    }
  };

  const redirectByRole = (role) => {
    if (role === "admin") {
      navigate("/admin");
    } else if (role === "seller") {
      navigate("/seller");
    } else {
      navigate("/buyer");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (!formData.full_name.trim()) {
      setError("Full name is required.");
      return;
    }

    if (!validateEmail(formData.email)) {
      setError("Please enter a valid email address.");
      return;
    }

    if (!validatePassword(formData.password)) {
      setError(
        "Password must include uppercase, lowercase, number, special character and minimum 8 characters."
      );
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setError("Password and confirm password do not match.");
      return;
    }

    try {
      setLoading(true);

      const tokenData = await registerUser({
        email: formData.email.trim(),
        password: formData.password,
        full_name: formData.full_name.trim(),
        phone: formData.phone.trim() || undefined,
        role: formData.role,
      });

      const {
        access_token,
        refresh_token,
      } = tokenData;

      saveAuthTokens(access_token, refresh_token);

      // register response me role nahi aa raha
      // is liye current user API se profile aur role get kar rahe hain

      const user = await getCurrentUser();

      saveUserRole(user.role);

      dispatch(
        loginSuccess({
          accessToken: access_token,
          refreshToken: refresh_token,
          role: user.role,
          user,
        })
      );

      redirectByRole(user.role);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-[#F5F5F5] flex items-center justify-center px-4 pt-32 pb-16">
        <div className="bg-white rounded-[28px] shadow-xl p-8 md:p-10 w-full max-w-2xl">
          <h1 className="font-heading text-4xl font-bold text-[#0A1A2F] text-center mb-8">
            Register
          </h1>

          {error && (
            <p className="bg-red-50 text-[#EF4444] text-sm text-center p-3 rounded-xl mb-5 md:col-span-2">
              {error}
            </p>
          )}

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 md:grid-cols-2 gap-5"
          >
            <input
              type="text"
              name="full_name"
              placeholder="Full Name"
              autoComplete="name"
              value={formData.full_name}
              onChange={handleChange}
              className="border border-gray-200 rounded-full px-5 py-3 outline-none focus:border-[#C9A03D]"
            />

            <input
              type="email"
              name="email"
              placeholder="Email"
              autoComplete="email"
              value={formData.email}
              onChange={handleChange}
              className="border border-gray-200 rounded-full px-5 py-3 outline-none focus:border-[#C9A03D]"
            />

            <input
              type="text"
              name="phone"
              placeholder="Phone Optional"
              autoComplete="tel"
              value={formData.phone}
              onChange={handleChange}
              className="border border-gray-200 rounded-full px-5 py-3 outline-none focus:border-[#C9A03D]"
            />

            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="border border-gray-200 rounded-full px-5 py-3 outline-none focus:border-[#C9A03D]"
            >
              <option value="buyer">Buyer</option>
              <option value="seller">Seller</option>
            </select>

            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                autoComplete="new-password"
                value={formData.password}
                onChange={handleChange}
                className="w-full border border-gray-200 rounded-full px-5 py-3 pr-12 outline-none focus:border-[#C9A03D]"
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-5 top-1/2 -translate-y-1/2 text-[#0A1A2F]/65 hover:text-[#0A1A2F] transition-all"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? (
                  <FaEyeSlash size={17} />
                ) : (
                  <FaEye size={17} />
                )}
              </button>
            </div>

            <div className="relative">
              <input
                type={showConfirmPassword ? "text" : "password"}
                name="confirm_password"
                placeholder="Confirm Password"
                autoComplete="new-password"
                value={formData.confirm_password}
                onChange={handleChange}
                className="w-full border border-gray-200 rounded-full px-5 py-3 pr-12 outline-none focus:border-[#C9A03D]"
              />

              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-5 top-1/2 -translate-y-1/2 text-[#0A1A2F]/65 hover:text-[#0A1A2F] transition-all"
                aria-label={
                  showConfirmPassword
                    ? "Hide confirm password"
                    : "Show confirm password"
                }
              >
                {showConfirmPassword ? (
                  <FaEyeSlash size={17} />
                ) : (
                  <FaEye size={17} />
                )}
              </button>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="md:col-span-2 bg-[#0A1A2F] text-white rounded-full py-3 text-xs font-bold uppercase tracking-widest hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all disabled:opacity-60"
            >
              {loading ? "Registering..." : "Register"}
            </button>
          </form>

          <p className="text-center text-sm mt-6">
            Already have an account?{" "}
            <Link
              to="/login"
              className="text-[#C9A03D] font-bold"
            >
              Login
            </Link>
          </p>
        </div>
      </section>

      <Footer />
    </>
  );
}

export default Register;