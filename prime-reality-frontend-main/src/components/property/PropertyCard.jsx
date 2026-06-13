import { Link } from "react-router-dom";

// property card
// listing page me har property ka card show hoga

function PropertyCard({ property }) {
  return (
    <div className="bg-white rounded-[28px] overflow-hidden shadow-lg border border-black/5 hover:shadow-2xl transition-all duration-300">
      <div className="relative h-64 overflow-hidden">
        <img
          src={property.image}
          alt={property.title}
          className="w-full h-full object-cover hover:scale-105 transition-all duration-500"
          loading="lazy"
          onError={(e) => {
            e.currentTarget.src =
              "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=900";
          }}
        />

        <span className="absolute top-4 left-4 bg-[#C9A03D] text-[#0A1A2F] text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">
          {property.type}
        </span>
      </div>

      <div className="p-6">
        <h3 className="font-heading text-2xl font-bold text-[#0A1A2F] mb-2">
          {property.title}
        </h3>

        <p className="text-sm text-[#333333] mb-3">
          {property.city}
        </p>

        <div className="flex items-center justify-between text-sm text-[#333333] mb-5">
          <span>{property.bedrooms} Beds</span>
          <span>{property.area}</span>
        </div>

        <div className="flex items-center justify-between">
          <p className="text-xl font-bold text-[#C9A03D]">
            ${property.price.toLocaleString()}
          </p>

          <Link
            to={`/properties/${property.id}`}
            className="bg-[#0A1A2F] text-white text-[10px] font-bold uppercase tracking-widest px-5 py-2.5 rounded-full hover:bg-[#C9A03D] hover:text-[#0A1A2F] transition-all"
          >
            View
          </Link>
        </div>
      </div>
    </div>
  );
}

export default PropertyCard;