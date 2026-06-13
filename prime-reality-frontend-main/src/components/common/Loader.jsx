// reusable loader component
// API loading aur page loading ke liye

function Loader() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F5F5F5]">
      <div className="w-14 h-14 border-4 border-[#C9A03D] border-t-transparent rounded-full animate-spin"></div>
    </div>
  );
}

export default Loader;