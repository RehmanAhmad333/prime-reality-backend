import PropertyCard from "./PropertyCard";

// property grid
// filtered properties ko responsive grid me show karega

function PropertyGrid({ properties }) {
  if (!properties.length) {
    return (
      <div className="bg-white rounded-[28px] p-10 text-center shadow-md">
        <h3 className="font-heading text-3xl font-bold text-[#0A1A2F] mb-3">
          No Properties Found
        </h3>

        <p className="text-[#333333]">
          Try changing your search or filter options.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
      {properties.map((property) => (
        <PropertyCard
          key={property.id}
          property={property}
        />
      ))}
    </div>
  );
}

export default PropertyGrid;