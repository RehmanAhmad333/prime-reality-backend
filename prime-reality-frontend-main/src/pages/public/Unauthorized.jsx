import { Link } from "react-router-dom";

// unauthorized page
// wrong role route access kare to yeh page show hoga

function Unauthorized() {
  return (
    <div className="min-h-screen bg-[#F5F5F5] flex items-center justify-center px-4">
      <div className="bg-white rounded-[28px] shadow-xl p-10 max-w-md w-full text-center">
        <h1 className="font-heading text-4xl font-bold text-[#0A1A2F] mb-4">
          Unauthorized Access
        </h1>

        <p className="text-[#333333] mb-8">
          You do not have permission to access this page.
        </p>

        <Link
          to="/login"
          className="inline-flex bg-[#0A1A2F] text-white px-7 py-3 rounded-full text-xs font-bold uppercase tracking-widest hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all"
        >
          Back To Login
        </Link>
      </div>
    </div>
  );
}

export default Unauthorized;