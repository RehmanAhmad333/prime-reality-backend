// reusable filter sidebar
// property listing page ke filters yahan se handle honge

function FilterSidebar({
  filters,
  onFilterChange,
  onApplyFilters,
  onResetFilters,
}) {
  return (
    <aside className="bg-white rounded-[28px] p-6 shadow-lg border border-black/5 space-y-5">
      <h3 className="font-heading text-2xl font-bold text-[#0A1A2F]">
        Filter Properties
      </h3>

      <select
        name="type"
        value={filters.type}
        onChange={onFilterChange}
        className="w-full border border-gray-200 rounded-full px-4 py-3 text-sm outline-none focus:border-[#C9A03D]"
      >
        <option value="">Property Type</option>
        <option value="apartment">Apartment</option>
        <option value="villa">Villa</option>
        <option value="land">Land</option>
        <option value="commercial">Commercial</option>
      </select>

      <select
        name="bedrooms"
        value={filters.bedrooms}
        onChange={onFilterChange}
        className="w-full border border-gray-200 rounded-full px-4 py-3 text-sm outline-none focus:border-[#C9A03D]"
      >
        <option value="">Bedrooms</option>
        <option value="1">1 Bedroom</option>
        <option value="2">2 Bedrooms</option>
        <option value="3">3 Bedrooms</option>
        <option value="4">4+ Bedrooms</option>
      </select>

      <input
        type="text"
        name="city"
        value={filters.city}
        onChange={onFilterChange}
        placeholder="City / Location"
        className="w-full border border-gray-200 rounded-full px-4 py-3 text-sm outline-none focus:border-[#C9A03D]"
      />

      <input
        type="number"
        name="minPrice"
        value={filters.minPrice}
        onChange={onFilterChange}
        placeholder="Min Price"
        className="w-full border border-gray-200 rounded-full px-4 py-3 text-sm outline-none focus:border-[#C9A03D]"
      />

      <input
        type="number"
        name="maxPrice"
        value={filters.maxPrice}
        onChange={onFilterChange}
        placeholder="Max Price"
        className="w-full border border-gray-200 rounded-full px-4 py-3 text-sm outline-none focus:border-[#C9A03D]"
      />

      <button
        type="button"
        onClick={onApplyFilters}
        className="w-full bg-[#0A1A2F] text-white rounded-full py-3 text-xs font-bold uppercase tracking-widest hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all duration-300"
      >
        Apply Filters
      </button>

      <button
        type="button"
        onClick={onResetFilters}
        className="w-full border border-[#0A1A2F] text-[#0A1A2F] rounded-full py-3 text-xs font-bold uppercase tracking-widest hover:bg-[#0A1A2F] hover:text-white transition-all duration-300"
      >
        Reset
      </button>
    </aside>
  );
}

export default FilterSidebar;