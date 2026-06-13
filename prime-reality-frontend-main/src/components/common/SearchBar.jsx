// reusable search bar
// property search ke liye clean and reusable component

function SearchBar({
  value,
  onChange,
  onSubmit,
  placeholder = "Search by city, title or location",
  buttonLabel = "Search",
  className = "",
}) {
  return (
    <form
      onSubmit={onSubmit}
      className={`w-full bg-white rounded-full p-1.5 flex items-center shadow-md border border-black/5 ${className}`}
    >
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="flex-1 bg-transparent px-5 py-3 text-[#0A1A2F] text-sm outline-none placeholder:text-gray-400"
      />

      <button
        type="submit"
        className="bg-[#0A1A2F] text-white rounded-full px-6 py-3 text-[11px] font-bold uppercase tracking-widest hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all duration-300"
      >
        {buttonLabel}
      </button>
    </form>
  );
}

export default SearchBar;