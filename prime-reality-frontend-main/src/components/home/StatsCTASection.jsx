import { useNavigate } from "react-router-dom";

import Button from "../common/Button";

// stats + CTA section
// design same rakha hai
// Book Now button login page pe redirect karega

function StatsCTASection() {
  const navigate = useNavigate();

  const stats = [
    {
      value: "12+ Million",
      text: "Buyer and seller use our network every month!",
    },
    {
      value: "12x More",
      text: "Visit than to the next land listing network.",
    },
    {
      value: "1+ Million",
      text: "Rural real estate to live in, entertain, build & invest!",
    },
  ];

  return (
    <section className="bg-[#F5F5F5] py-20">
      <div className="container-custom grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
        {/* stats */}
        <div className="lg:col-span-3 space-y-8">
          {stats.map((stat) => (
            <div key={stat.value} className="border-b border-[#0A1A2F]/20 pb-5">
              <h3 className="font-heading text-3xl font-bold uppercase text-[#0A1A2F] mb-2">
                {stat.value}
              </h3>

              <p className="text-[11px] uppercase tracking-wider text-[#333333] leading-5">
                {stat.text}
              </p>
            </div>
          ))}
        </div>

        {/* image */}
        <div className="lg:col-span-4">
          <div className="rounded-[32px] overflow-hidden shadow-2xl">
            <img
              src="https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?auto=format&fit=crop&q=80&w=800"
              alt="Luxury property CTA"
              className="w-full h-[520px] object-cover"
              loading="lazy"
            />
          </div>
        </div>

        {/* CTA */}
        <div className="lg:col-span-5">
          <h2 className="font-heading text-4xl md:text-5xl font-bold uppercase text-[#0A1A2F] leading-tight mb-6">
            Team Up With Us <br />
            Build Better
          </h2>

          <p className="text-sm text-[#333333] uppercase tracking-wider leading-8 max-w-xl mb-8">
            Partner with us to bring your vision to life with unmatched
            expertise and dedication. Together, we’ll create spaces that inspire
            and elevate the way you live, work, and play.
          </p>

          <Button
            text="Book Now"
            variant="primary"
            onClick={() => navigate("/login")}
          />
        </div>
      </div>
    </section>
  );
}

export default StatsCTASection;