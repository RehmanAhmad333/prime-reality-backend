import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";

import Navbar from "../../components/common/Navbar";
import Footer from "../../components/common/Footer";
import SearchBar from "../../components/common/SearchBar";
import FilterSidebar from "../../components/common/FilterSidebar";
import PropertyGrid from "../../components/property/PropertyGrid";

// mock data
// backend live hone ke baad yahi data API se replace hoga

const mockProperties = [
  {
    id: 1,
    title: "Luxury 3-BHK Villa",
    city: "Karachi",
    type: "villa",
    bedrooms: 3,
    price: 230000,
    area: "3200 sq ft",
    image:
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=900",
  },
  {
    id: 2,
    title: "Modern Apartment",
    city: "Lahore",
    type: "apartment",
    bedrooms: 2,
    price: 120000,
    area: "1400 sq ft",
    image:
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&q=80&w=900",
  },
  {
    id: 3,
    title: "Commercial Office Space",
    city: "Islamabad",
    type: "commercial",
    bedrooms: 1,
    price: 450000,
    area: "5000 sq ft",
    image:
      "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=900",
  },
  {
    id: 4,
    title: "Premium Residential Land",
    city: "Karachi",
    type: "land",
    bedrooms: 0,
    price: 85000,
    area: "240 sq yd",
    image:
      "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=900",
  },
];

function Properties() {
  const [searchParams] = useSearchParams();

  const initialFilters = {
    type: searchParams.get("type") || "",
    bedrooms: "",
    city: searchParams.get("city") || "",
    minPrice: "",
    maxPrice: "",
  };

  const [searchTerm, setSearchTerm] = useState("");

  const [filters, setFilters] = useState(initialFilters);

  const [appliedFilters, setAppliedFilters] = useState(initialFilters);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;

    setFilters({
      ...filters,
      [name]: value,
    });
  };

  const handleApplyFilters = () => {
    setAppliedFilters(filters);
  };

  const handleResetFilters = () => {
    const emptyFilters = {
      type: "",
      bedrooms: "",
      city: "",
      minPrice: "",
      maxPrice: "",
    };

    setFilters(emptyFilters);
    setAppliedFilters(emptyFilters);
    setSearchTerm("");
  };

  const filteredProperties = useMemo(() => {
    return mockProperties.filter((property) => {
      const searchMatch =
        property.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.city.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.type.toLowerCase().includes(searchTerm.toLowerCase());

      const typeMatch =
        !appliedFilters.type || property.type === appliedFilters.type;

      const cityMatch =
        !appliedFilters.city ||
        property.city
          .toLowerCase()
          .includes(appliedFilters.city.toLowerCase());

      const bedroomMatch =
        !appliedFilters.bedrooms ||
        Number(property.bedrooms) >= Number(appliedFilters.bedrooms);

      const minPriceMatch =
        !appliedFilters.minPrice ||
        property.price >= Number(appliedFilters.minPrice);

      const maxPriceMatch =
        !appliedFilters.maxPrice ||
        property.price <= Number(appliedFilters.maxPrice);

      return (
        searchMatch &&
        typeMatch &&
        cityMatch &&
        bedroomMatch &&
        minPriceMatch &&
        maxPriceMatch
      );
    });
  }, [searchTerm, appliedFilters]);

  return (
    <>
      <Navbar />

      <main className="bg-[#F5F5F5] min-h-screen pt-32 pb-20">
        <section className="container-custom">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h1 className="font-heading text-5xl md:text-6xl font-bold text-[#0A1A2F] mb-5">
              Explore Land
            </h1>

            <p className="text-[#333333] leading-7">
              Search and filter premium properties based on price, location,
              type and bedrooms.
            </p>
          </div>

          <div className="max-w-3xl mx-auto mb-12">
            <SearchBar
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onSubmit={handleSearchSubmit}
              placeholder="Search by title, city or type"
              buttonLabel="Search"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div className="lg:col-span-3">
              <FilterSidebar
                filters={filters}
                onFilterChange={handleFilterChange}
                onApplyFilters={handleApplyFilters}
                onResetFilters={handleResetFilters}
              />
            </div>

            <div className="lg:col-span-9">
              <PropertyGrid properties={filteredProperties} />
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
}

export default Properties;