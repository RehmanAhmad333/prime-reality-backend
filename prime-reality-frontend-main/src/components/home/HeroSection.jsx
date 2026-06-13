import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Button from "../common/Button";

// hero section
// design same rakha hai
// hero search ab properties page ke filters ke sath connect hai

function HeroSection() {
  const navigate = useNavigate();

  const [propertyType, setPropertyType] = useState("");
  const [location, setLocation] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();

    const params = new URLSearchParams();

    if (propertyType) {
      params.set("type", propertyType);
    }

    if (location) {
      params.set("city", location);
    }

    navigate(`/properties?${params.toString()}`);
  };

  return (
    <section className="relative min-h-screen bg-[#F5F5F5] overflow-hidden pt-28 pb-16">
      {/* light luxury background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(10,26,47,0.08),transparent_30%),linear-gradient(135deg,rgba(201,160,61,0.08),transparent_35%)]"></div>

      <div className="container-custom relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* left content */}
          <div>
            <h1 className="font-heading text-5xl md:text-6xl lg:text-7xl font-bold leading-[0.95] text-[#0A1A2F] mb-6">
              Discover Your <br />
              Dream Home <br />
              Heart of Luxury
            </h1>

            <p className="max-w-xl text-sm md:text-base text-[#333333] leading-8 mb-8">
              Step into a world of unparalleled elegance and sophistication. Our
              curated selection of luxury properties offers the finest living
              spaces, designed to exceed your expectations.
            </p>

            {/* small price image card */}
            <div className="relative max-w-xl rounded-[28px] overflow-hidden shadow-2xl mb-8">
              <img
                src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&q=80&w=900"
                alt="Luxury apartment"
                className="w-full h-56 object-cover"
                loading="eager"
              />

              <div className="absolute top-4 right-4 bg-[#C9A03D] text-white px-5 py-3 rounded-md shadow-lg">
                <p className="text-[10px] font-bold uppercase text-white">
                  Price Started At
                </p>
                <p className="text-2xl md:text-3xl font-extrabold">
                  $2,300,00
                </p>
              </div>
            </div>
          </div>

          {/* right property highlight */}
          <div className="relative">
            <div className="relative rounded-[36px] overflow-hidden shadow-2xl">
              <img
                src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&q=80&w=1000"
                alt="Luxury home"
                className="w-full h-[560px] object-cover"
                loading="eager"
              />

              <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent"></div>

              <div className="absolute bottom-8 left-8 right-8 text-white">
                <h2 className="font-heading text-3xl font-bold uppercase mb-3">
                  Live The City Life
                </h2>

                <p className="text-xs uppercase tracking-widest leading-6 max-w-lg mb-5">
                  Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna.
                </p>

                <form
                  onSubmit={handleSearch}
                  className="flex flex-col sm:flex-row gap-3"
                >
                  <select
                    value={propertyType}
                    onChange={(e) => setPropertyType(e.target.value)}
                    className="bg-black/40 border border-white/40 text-white rounded-full px-4 py-3 text-[10px] uppercase outline-none"
                  >
                    <option value="">Select Type</option>
                    <option value="villa">Villa</option>
                    <option value="apartment">Apartment</option>
                    <option value="land">Land</option>
                    <option value="commercial">Commercial</option>
                  </select>

                  <select
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="bg-black/40 border border-white/40 text-white rounded-full px-4 py-3 text-[10px] uppercase outline-none"
                  >
                    <option value="">Location</option>
                    <option value="karachi">Karachi</option>
                    <option value="lahore">Lahore</option>
                    <option value="islamabad">Islamabad</option>
                  </select>

                  <button
                    type="submit"
                    className="bg-white text-[#0A1A2F] rounded-full px-5 py-3 text-[10px] font-bold uppercase hover:bg-[#C9A03D] transition-all"
                  >
                    Search Here
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>

        {/* CTA buttons */}
        <div className="mt-8 flex gap-4">
          <Button
            text="Explore Land"
            variant="primary"
            onClick={() => navigate("/properties")}
          />

          <Button
            text="Book Now"
            variant="outline"
            onClick={() => navigate("/login")}
          />
        </div>
      </div>
    </section>
  );
}

export default HeroSection;