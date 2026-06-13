import React, { useState } from 'react';
import Footer from '../../components/common/Footer';

const ContactUs = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const validateForm = () => {
    let tempErrors = {};
    if (!formData.name.trim()) tempErrors.name = "USERNAME IS REQUIRED";
    
    if (!formData.email.trim()) {
      tempErrors.email = "EMAIL ADDRESS IS REQUIRED";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      tempErrors.email = "INVALID EMAIL PATTERN";
    }
    
    if (!formData.message.trim()) tempErrors.message = "YOUR MESSAGE IS REQUIRED";

    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      setSubmitted(true);
      setFormData({ name: '', email: '', message: '' });
      setTimeout(() => setSubmitted(false), 4000);
    }
  };

  return (
    <section 
      className="bg-[#F4F6F9] min-h-screen w-full font-inter text-[#0A1A2F] flex flex-col overflow-x-hidden overflow-y-auto relative"
      style={{
        backgroundImage: 'linear-gradient(135deg, #F4F6F9 0%, #EAEFF5 100%)',
        msOverflowStyle: 'none',
        scrollbarWidth: 'none'
      }}
    >
      {/* Scrollbar hidden styling */}
      <style dangerouslySetInnerHTML={{__html: `
        html::-webkit-scrollbar,
        body::-webkit-scrollbar,
        section::-webkit-scrollbar {
          display: none !important;
          width: 0 !important;
          background: transparent !important;
        }
        html, body, #root {
          overflow-x: hidden !important;
          margin: 0 !important;
          padding: 0 !important;
        }
      `}} />

      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-white/60 via-transparent to-transparent pointer-events-none"></div>

      {/* Main Content Area */}
      <div className="max-w-5xl w-full mx-auto relative z-10 flex flex-col items-center py-16 px-4 sm:px-8 lg:px-20 flex-grow">
        
        {/* HEADER BLOCK */}
        <div className="text-center mb-12">
          <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-bold tracking-[0.2em] text-[#0A1A2F] uppercase">
            CONTACT APPROACH FORM
          </h1>
          <div className="h-[3px] w-24 bg-[#C5A880] mx-auto mt-4 rounded-full"></div>
        </div>
        
        {/* MAIN UI GRID CONTAINER */}
        <div className="grid grid-cols-1 lg:grid-cols-2 w-full gap-8 max-w-4xl mb-12">
          
          {/* LEFT SIDE: FORM BLOCK */}
          <div className="bg-white p-10 sm:p-14 rounded-2xl shadow-[0_15px_40px_rgba(0,0,0,0.06)] border border-gray-100 flex flex-col justify-between">
            <div>
              <h2 className="text-xl font-bold tracking-widest text-[#0A1A2F] uppercase mb-12 border-b border-gray-100 pb-4">
                GET IN TOUCH
              </h2>
              
              {submitted && (
                <div className="mb-6 p-3 bg-[#0A1A2F] text-[#C5A880] text-xs font-bold tracking-widest rounded-lg uppercase shadow-sm text-center">
                  ✓ MESSAGE SENT SUCCESSFULLY
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-12">
                <div className="flex flex-col space-y-2">
                  <div className="flex items-center space-x-4 border-b-2 border-gray-200 pb-2 focus-within:border-[#0A1A2F] transition duration-300">
                    <span className="text-[#0A1A2F]/50 text-sm">👤</span>
                    <input 
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="Username"
                      className="w-full bg-transparent border-none text-sm font-semibold text-[#0A1A2F] focus:outline-none tracking-wider placeholder-gray-400"
                    />
                  </div>
                  {errors.name && <span className="text-red-500 text-[10px] font-bold tracking-wider uppercase mt-1">{errors.name}</span>}
                </div>

                <div className="flex flex-col space-y-2">
                  <div className="flex items-center space-x-4 border-b-2 border-gray-200 pb-2 focus-within:border-[#0A1A2F] transition duration-300">
                    <span className="text-[#0A1A2F]/50 text-sm">✉</span>
                    <input 
                      type="text"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="Youremail@email.com"
                      className="w-full bg-transparent border-none text-sm font-semibold text-[#0A1A2F] focus:outline-none tracking-wider placeholder-gray-400"
                    />
                  </div>
                  {errors.email && <span className="text-red-500 text-[10px] font-bold tracking-wider uppercase mt-1">{errors.email}</span>}
                </div>

                <div className="flex flex-col space-y-2">
                  <div className="flex items-start space-x-4 border-b-2 border-gray-200 pb-2 focus-within:border-[#0A1A2F] transition duration-300">
                    <span className="text-[#0A1A2F]/50 text-sm mt-1">💬</span>
                    <textarea 
                      rows="3"
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      placeholder="Your Message"
                      className="w-full bg-transparent border-none text-sm font-semibold text-[#0A1A2F] focus:outline-none tracking-wider resize-none placeholder-gray-400 leading-relaxed"
                    ></textarea>
                  </div>
                  {errors.message && <span className="text-red-400 text-[10px] font-bold tracking-wider uppercase mt-1">{errors.message}</span>}
                </div>

                <button 
                  type="submit" 
                  className="w-full h-14 bg-gradient-to-r from-[#0A1A2F] to-[#1F3E56] hover:from-[#C5A880] hover:to-[#b3956b] text-white hover:text-[#0A1A2F] font-bold text-xs tracking-[0.3em] rounded-xl shadow-xl transition-all duration-500 flex items-center justify-center space-x-3 cursor-pointer mt-8"
                >
                  <span className="uppercase">SEND INQUIRY</span>
                  <span className="text-sm">➔</span>
                </button>
              </form>
            </div>
          </div>

          {/* RIGHT SIDE: LOCATE US (FIXED PRODUCTION MAP LINK) */}
          <div className="bg-white p-10 sm:p-14 rounded-2xl shadow-[0_15px_40px_rgba(0,0,0,0.06)] border border-gray-100 flex flex-col justify-between">
            <div className="w-full space-y-4">
              <div className="text-xs font-bold tracking-widest text-[#0A1A2F] uppercase border-l-4 border-[#C5A880] pl-3">
                LOCATE US
              </div>
              
              {/* 🌐 FIXED AND SECURE GOOGLE MAPS EMBED URL */}
              <div className="h-48 rounded-xl overflow-hidden bg-gray-100 border border-gray-200/80 shadow-inner relative">
                <iframe 
                  title="Casablanca Morocco HQ Office Location"
                  src="https://maps.google.com/maps?q=Casablanca,%20Morocco&t=&z=13&ie=UTF8&iwloc=&output=embed" 
                  className="w-full h-full border-0"
                  allowFullScreen={true}
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                ></iframe>
              </div>
            </div>

            {/* DETAILS */}
            <div className="text-center space-y-4 pt-6">
              <div className="space-y-1">
                <p className="text-[#0A1A2F] text-sm font-bold tracking-widest">BD 2 MARS, N1 136,</p>
                <p className="text-[#0A1A2F] text-sm font-bold tracking-widest">MOROCCO CASABLANCA</p>
              </div>
              <p className="text-[#C5A880] text-sm font-bold tracking-widest">+212 522 275 386</p>
              <p className="text-gray-500 text-xs font-semibold tracking-widest break-all underline underline-offset-4 decoration-[#C5A880]/40">
                INFO@PRIMEREALITY.COM
              </p>
            </div>

            {/* SOCIALS */}
            <div className="pt-8 border-t border-gray-100">
              <p className="text-center text-[10px] text-gray-400 tracking-[0.3em] uppercase mb-5">CATCH ON SOCIAL</p>
              <div className="flex justify-center items-center space-x-8 font-bold text-xs text-[#0A1A2F]/70">
                <a href="#fb" className="hover:text-[#C5A880] transition duration-300">FB</a>
                <a href="#tw" className="hover:text-[#C5A880] transition duration-300">TW</a>
                <a href="#ig" className="hover:text-[#C5A880] transition duration-300">IG</a>
                <a href="#ln" className="hover:text-[#C5A880] transition duration-300">LN</a>
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* FOOTER */}
      <Footer />
    </section>
  );
};

export default ContactUs;