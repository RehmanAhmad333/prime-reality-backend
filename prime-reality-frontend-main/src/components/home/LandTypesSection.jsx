// land type section
// design ke middle cards jaisa layout banaya hai

const landTypes = [
  {
    id: 1,
    title: "Build The Home Of Your Dreams",
    image:
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=700",
  },
  {
    id: 2,
    title: "Shape Your Business Future",
    image:
      "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=700",
  },
  {
    id: 3,
    title: "Foundation For Industry",
    image:
      "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&q=80&w=700",
  },
];

function LandTypesSection() {
  return (
    <section className="bg-[#F5F5F5] py-20">
      <div className="container-custom">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start mb-14">
          <h2 className="font-heading text-4xl md:text-5xl font-bold uppercase text-[#0A1A2F] leading-tight">
            Different Type Of <br />
            Land Available
          </h2>

          <p className="text-sm text-[#333333] uppercase tracking-wider leading-8 max-w-xl">
            Build your dream home on a prime piece of residential land,
            perfectly situated in family-friendly neighborhoods, these plots
            offer the ideal foundation for your future.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-end">
          {landTypes.map((item, index) => (
            <div
              key={item.id}
              className={`relative overflow-hidden rounded-[28px] shadow-2xl ${
                index === 1 ? "md:translate-y-[-45px]" : ""
              }`}
            >
              <img
                src={item.image}
                alt={item.title}
                className="w-full h-[360px] md:h-[420px] object-cover"
                loading="lazy"
                onError={(e) => {
                  e.currentTarget.src =
                    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=700";
                }}
              />

              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/10 to-transparent"></div>

              <h3 className="absolute bottom-6 left-6 right-6 font-heading text-xl font-bold text-white uppercase leading-tight">
                {item.title}
              </h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default LandTypesSection;