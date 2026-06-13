import { Link, NavLink } from "react-router-dom";

// reusable navbar
// final design ke according navbar same rakha hai
// login/register navbar me add nahi kar rahe because design me nahi hai

function Navbar() {
  const navLinks = [
    { label: "HOME", path: "/" },
    { label: "EXPLORE LAND", path: "/properties" },
    { label: "SERVICE", path: "/services" },
    { label: "ADVERTISE", path: "/advertise" },
  ];

  return (
    <header className="absolute top-0 left-0 w-full z-50">
      <nav className="container-custom h-24 flex items-center justify-between">
        {/* logo */}
        <Link to="/" className="flex items-center">
          <svg
            className="w-14 h-14 text-[#0A1A2F]"
            viewBox="0 0 100 100"
            fill="none"
            stroke="currentColor"
            strokeWidth="3"
          >
            <path d="M20 82 V42 L42 24 V82" />
            <path d="M42 82 V16 L62 34 V82" />
            <path d="M62 82 V48 L82 58 V82" />
            <path d="M14 82 H88" />
          </svg>
        </Link>

        {/* center links */}
        <ul className="hidden lg:flex items-center gap-8 text-[10px] font-bold tracking-widest text-[#0A1A2F] uppercase">
          {navLinks.map((link) => (
            <li key={link.path}>
              <NavLink
                to={link.path}
                className={({ isActive }) =>
                  `transition-all duration-300 ${
                    isActive ? "text-[#C9A03D]" : "hover:text-[#C9A03D]"
                  }`
                }
              >
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>

        {/* right actions */}
        <div className="hidden md:flex items-center gap-5">
          <Link
            to="/contact"
            className="text-[10px] font-bold tracking-widest text-[#0A1A2F] uppercase hover:text-[#C9A03D] transition-all"
          >
            Contact Us
          </Link>

          <Link
            to="/login"
            className="bg-[#0A1A2F] text-white text-[10px] font-bold tracking-widest uppercase px-7 py-3 rounded-full hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all duration-300"
          >
            Book Now
          </Link>
        </div>

        {/* mobile menu placeholder */}
        <button
          type="button"
          className="lg:hidden text-[#0A1A2F] text-2xl font-bold"
          aria-label="Open menu"
        >
          ☰
        </button>
      </nav>
    </header>
  );
}

export default Navbar;