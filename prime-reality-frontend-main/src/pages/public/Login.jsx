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
  loginUser,
  getCurrentUser,
} from "../../services/authService";

import {
  saveAuthTokens,
  saveUserRole,
} from "../../utils/helpers/authHelper";

import { validateEmail } from "../../utils/validators/authValidator";

import { loginSuccess } from "../../store/slices/authSlice";

// login page
// yahan complete login flow handle ho raha hai
// login -> token save -> user profile fetch -> role save -> dashboard redirect

function Login() {
  const navigate = useNavigate();

  const dispatch = useDispatch();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);

  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  // input change handler
  // state update karega aur previous error clear karega

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));

    if (error) {
      setError("");
    }
  };

  // role ke hisaab se dashboard redirect

  const redirectByRole = (role) => {
    switch (role) {
      case "admin":
        navigate("/admin");
        break;

      case "seller":
        navigate("/seller");
        break;

      case "buyer":
      default:
        navigate("/buyer");
        break;
    }
  };

  // login submit handler
  const handleSubmit = async (e) => {
    e.preventDefault();

    // multiple clicks prevent karne ke liye

    if (loading) return;

    setError("");

    const email = formData.email.trim();

    // login pe password strength check nahi kar rahe
    // backend email/password verify karega

    if (!validateEmail(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    if (!formData.password.trim()) {
      setError("Please enter your password.");
      return;
    }

    try {
      setLoading(true);

      // login API call

      const tokenData = await loginUser({
        email,
        password: formData.password,
      });

      const {
        access_token,
        refresh_token,
      } = tokenData;

      // access token aur refresh token save

      saveAuthTokens(
        access_token,
        refresh_token
      );

      // current user profile fetch
      // backend login response me role nahi aa raha

      const user = await getCurrentUser();

      // role separate save kar rahe hain

      saveUserRole(user.role);

      // redux auth state update

      dispatch(
        loginSuccess({
          accessToken: access_token,
          refreshToken: refresh_token,
          role: user.role,
          user,
        })
      );

      // dashboard redirect

      redirectByRole(user.role);
    } catch (err) {
      if (err.code === "ECONNABORTED") {
        setError(
          "Connection timed out. Please try again."
        );

        return;
      }

      setError(
        err?.response?.data?.detail ||
          "Invalid email or password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* navbar */}

      <Navbar />

      <section className="min-h-screen bg-[#F5F5F5] flex items-center justify-center px-4 pt-32 pb-16">
        <div className="w-full max-w-md bg-white rounded-[28px] shadow-xl p-8 md:p-10">

          {/* page heading */}

          <h1 className="font-heading text-4xl font-bold text-[#0A1A2F] text-center mb-8">
            Login
          </h1>

          {/* error message */}

          {error && (
            <p className="bg-red-50 text-red-500 text-sm text-center p-3 rounded-xl mb-5">
              {error}
            </p>
          )}

          {/* login form */}

          <form
            onSubmit={handleSubmit}
            className="space-y-5"
          >
            {/* email input */}

            <input
              type="email"
              name="email"
              required
              autoComplete="email"
              placeholder="Enter Email"
              value={formData.email}
              onChange={handleChange}
              className="w-full border border-gray-200 rounded-full px-5 py-3 outline-none focus:border-[#C9A03D]"
            />

            {/* password input with eye icon */}

            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                required
                autoComplete="current-password"
                placeholder="Enter Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full border border-gray-200 rounded-full px-5 py-3 pr-14 outline-none focus:border-[#C9A03D]"
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-5 top-1/2 -translate-y-1/2 text-gray-500 hover:text-[#0A1A2F] transition-colors"
                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }
              >
                {showPassword ? (
                  <FaEyeSlash size={18} />
                ) : (
                  <FaEye size={18} />
                )}
              </button>
            </div>

            {/* submit button */}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#0A1A2F] text-white rounded-full py-3 text-xs font-bold uppercase tracking-widest hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading
                ? "Logging In..."
                : "Login"}
            </button>
          </form>

          {/* register page redirect */}

          <p className="text-center text-sm mt-6">
            Don&apos;t have an account?{" "}
            <Link
              to="/register"
              className="text-[#C9A03D] font-bold hover:underline"
            >
              Register
            </Link>
          </p>
        </div>
      </section>

      {/* footer */}

      <Footer />
    </>
  );
}

export default Login;