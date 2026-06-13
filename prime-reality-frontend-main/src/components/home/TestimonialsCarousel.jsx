import React, { useState } from 'react';

// 1. Multiple array items add kar diye hain dynamic premium images ke sath
const testimonialsData = [
  {
    id: 1,
    quote: "“ THEY DID AN AMAZING WORK FOR OUR HOME ”",
    feedback: "WORKING WITH THIS REAL ESTATE AGENCY WAS A SEAMLESS AND THE EXPERIENCE FROM START TO FINISH THEY UNDERSTOOD OUR NEED FOR A SPACE THAT COULD SERVE AS BOTH A COMFORTABLE HOME AND A PRODUCTIVE WORK ENVIRONMENT.",
    author: "DORIS D. SNELL",
    role: "RENTAL PROPERTY OWNER",
    userImage: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=200",
    bgImage: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=600",
    frontImage: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&q=80&w=600"
  },
  {
    id: 2,
    quote: "“ THE BEST ARCHITECTURAL PARTNERSHIP ”",
    feedback: "THEIR ATTENTION TO STRUCTURAL INTEGRITY AND BESPOKE LUXURY DESIGN EXCEEDED OUR EXPECTATIONS. EVERY CORNER REFLECTS MODERN MINIMALISM AND FUNCTIONAL ELEGANCE. HIGHLY RECOMMENDED FOR CORPORATE PROJECTS.",
    author: "ALEXANDER VANCE",
    role: "PORTFOLIO INVESTOR",
    userImage: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&q=80&w=200",
    bgImage: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&q=80&w=600",
    frontImage: "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&q=80&w=600"
  },
  {
    id: 3,
    quote: "“ EXCEPTIONAL BESPOKE PROPERTY CARE ”",
    feedback: "FROM MANAGING ACQUISITIONS TO FINAL ARCHITECTURAL TOUCHES, THE SYSTEM PROVIDED OUTSTANDING TRANSPARENCY. COMMUNICATION WAS CRISP, AND THE RESULTING ASSET VALUE HAS INCREASED SIGNIFICANTLY.",
    author: "SARAH JENNINGS",
    role: "CREATIVE DIRECTOR",
    userImage: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200",
    bgImage: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=600",
    frontImage: "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&q=80&w=600"
  }
];

const TestimonialsCarousel = () => {
  // 2. State management slider ko chalane ke liye
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === testimonialsData.length - 1 ? 0 : prevIndex + 1
    );
  };

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === 0 ? testimonialsData.length - 1 : prevIndex - 1
    );
  };

  // Current item data destructuring
  const { quote, feedback, author, role, userImage, bgImage, frontImage } = testimonialsData[currentIndex];

  return (
    <section className="bg-white py-20 px-6 md:px-12 lg:px-24 font-inter relative overflow-hidden">
      <div className="max-w-7xl mx-auto">
        
        {/* Header Block: Title and Functional Navigation Arrows */}
        <div className="flex items-center justify-between mb-12">
          <h2 className="font-serif text-3xl md:text-4xl font-normal text-[#1F3E56] tracking-wide uppercase">
            SATISFIED CLIENTS SPEAK
          </h2>
          
          {/* Functional Navigation Buttons */}
          <div className="flex space-x-3">
            <button 
              onClick={prevSlide}
              className="w-11 h-11 rounded-full bg-[#1F3E56] text-white flex items-center justify-center font-bold text-xl hover:bg-[#C5A880] transition duration-300 cursor-pointer shadow-md select-none"
              aria-label="Previous Slide"
            >
              ‹
            </button>
            <button 
              onClick={nextSlide}
              className="w-11 h-11 rounded-full bg-[#1F3E56] text-white flex items-center justify-center font-bold text-xl hover:bg-[#C5A880] transition duration-300 cursor-pointer shadow-md select-none"
              aria-label="Next Slide"
            >
              ›
            </button>
          </div>
        </div>

        {/* Split Grid Content Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          {/* Left Block: Dynamic Overlapping Images */}
          <div className="relative h-[380px] md:h-[450px] w-full flex items-center animate-fade-in">
            {/* Background Image (Grayed out) */}
            <div className="absolute left-0 top-0 w-[65%] h-[82%] overflow-hidden rounded-3xl shadow-md grayscale transition-all duration-500">
              <img 
                src={bgImage} 
                alt="Architecture Framework" 
                className="w-full h-full object-cover"
              />
            </div>
            {/* Front Image (Main asset focus with white frame border) */}
            <div className="absolute right-4 md:right-8 bottom-0 w-[65%] h-[82%] overflow-hidden rounded-3xl border-[6px] border-white shadow-2xl transition-all duration-500">
              <img 
                src={frontImage} 
                alt="Bespoke Design Presentation" 
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          {/* Right Block: Content Details */}
          <div className="space-y-6 lg:pl-6 min-h-[300px] flex flex-col justify-center">
            <h3 className="font-serif text-2xl md:text-3xl font-bold text-[#0A1A2F] leading-snug tracking-wide uppercase">
              {quote}
            </h3>
            <p className="text-gray-500 text-sm md:text-base leading-relaxed tracking-widest font-normal text-justify uppercase">
              {feedback}
            </p>
            
            {/* Decorative Divider bar */}
            <div className="w-24 h-[1px] bg-gray-300"></div>
            
            {/* User Meta Identity Grid */}
            <div className="flex items-center space-x-4 pt-2">
              <img 
                src={userImage} 
                alt={author} 
                className="w-12 h-12 rounded-full object-cover border border-[#0A1A2F]/20"
              />
              <div className="flex flex-col">
                <h4 className="font-bold text-[#0A1A2F] text-sm md:text-base tracking-wider uppercase">
                  {author}
                </h4>
                <p className="text-gray-400 text-xs tracking-widest font-medium uppercase mt-0.5">
                  {role}
                </p>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
};

export default TestimonialsCarousel;