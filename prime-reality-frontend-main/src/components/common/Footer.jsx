import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-[#1F3E56] text-white font-inter pt-14 pb-6 px-6 md:px-12 lg:px-24 border-t border-[#2A4E6C]">
      <div className="max-w-7xl mx-auto">
        
        {/* Top & Middle Section Combo */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 pb-12 items-start">
          
          {/* Left Column Group: Logo, Navigation, and Address (Takes 6 cols) */}
          <div className="lg:col-span-6 space-y-8">
            {/* Outline Structural Logo Asset */}
            <div className="flex items-center">
              <svg className="w-24 h-24 text-white" viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M20 80 V40 L40 25 V80" />
                <path d="M40 80 V20 L60 35 V80" />
                <path d="M60 80 V45 L80 55 V80" />
                <path d="M15 80 H85" />
              </svg>
            </div>

            {/* Flat Inline Navigation Row */}
            <div className="flex flex-wrap gap-x-6 gap-y-2 text-xs font-bold tracking-widest text-white">
              <a href="#home" className="hover:opacity-80 transition">HOME</a>
              <a href="#explore-land" className="hover:opacity-80 transition">EXPLORE LAND</a>
              <a href="#service" className="hover:opacity-80 transition">SERVICE</a>
              <a href="#advertise" className="hover:opacity-80 transition">ADVERTISE</a>
            </div>

            {/* Split Contact Meta Group */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-xs tracking-wider">
              {/* Address Container */}
              <div className="space-y-2">
                <p className="font-bold tracking-widest">ADDRESS:</p>
                <div className="text-gray-200 space-y-1 font-light">
                  <p>1234 ELM STREET, SUITE 567</p>
                  <p>SPRINGFIELD, IL 62704</p>
                </div>
              </div>

              {/* Phone Container */}
              <div className="space-y-2">
                <p className="font-bold tracking-widest">PHONE:</p>
                <div className="text-gray-200 space-y-1 font-light">
                  <p>PRIMARY: (123) 456-7890</p>
                  <p>SECONDARY: (987) 654-3210</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column Group: Action Bar & Social Pills (Takes 6 cols) */}
          <div className="lg:col-span-6 flex flex-col items-start lg:items-end space-y-8 w-full lg:text-right">
            {/* Large Accent Header */}
            <h2 className="font-serif text-2xl md:text-3xl lg:text-4xl font-normal tracking-wide text-white leading-tight max-w-md lg:text-left">
              READY TO FIND YOUR PERFECT & LUXURY PROPERTY?
            </h2>

            {/* Full Pill Search Structure */}
            <div className="relative w-full max-w-xl bg-white rounded-full p-1 flex items-center">
              <input 
                type="text" 
                placeholder="FIND YOUR PROPERTY" 
                className="w-full bg-transparent text-[#1F3E56] font-semibold text-xs tracking-widest pl-6 pr-12 py-3 rounded-full focus:outline-none placeholder-gray-400"
              />
              <button className="absolute right-2 bg-[#1F3E56] hover:bg-[#152B3C] text-white w-9 h-9 rounded-full flex items-center justify-center transition">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>

            {/* Inline Capsule Social Profiles Row */}
            <div className="flex flex-wrap gap-3 w-full justify-start lg:justify-end">
              {/* Facebook Button */}
              <a href="#facebook" className="border border-white/60 rounded-full px-4 py-2 flex items-center space-x-3 text-[10px] tracking-widest font-bold uppercase hover:bg-white hover:text-[#1F3E56] transition">
                <span>FACEBOOK</span>
                <span className="bg-white text-[#1F3E56] rounded-full w-4 h-4 flex items-center justify-center text-[8px]">f</span>
              </a>

              {/* Instagram Button */}
              <a href="#instagram" className="border border-white/60 rounded-full px-4 py-2 flex items-center space-x-3 text-[10px] tracking-widest font-bold uppercase hover:bg-white hover:text-[#1F3E56] transition">
                <span>INSTAGRAM</span>
                <span className="border border-[#1F3E56] bg-white text-[#1F3E56] rounded-full w-4 h-4 flex items-center justify-center text-[8px]">📸</span>
              </a>

              {/* Email Button */}
              <a href="#email" className="border border-white/60 rounded-full px-4 py-2 flex items-center space-x-3 text-[10px] tracking-widest font-bold uppercase hover:bg-white hover:text-[#1F3E56] transition">
                <span>EMAIL</span>
                <span className="text-white text-xs">✉</span>
              </a>
            </div>
          </div>

        </div>

        {/* Flat Fine Copyright Baseline */}
        <div className="border-t border-white/40 pt-6 text-[11px] font-medium tracking-widest text-white/90">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <a href="#privacy" className="hover:underline uppercase">PRIVACY AND POLICY</a>
            <p className="uppercase">COPYRIGHT BY PRIME REALITY 2024!</p>
            <a href="#terms" className="hover:underline uppercase">TERM & CONDITION</a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;