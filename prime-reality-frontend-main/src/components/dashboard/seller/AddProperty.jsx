// src/components/dashboard/seller/AddProperty.jsx
import React from 'react';

const AddProperty = ({ 
  formData = {},
  handleInputChange, 
  handleImageChange, 
  propertyImages = [], 
  removeImage, 
  handleFormSubmit 
}) => {
  return (
    <div className="bg-white p-8 md:p-12 rounded-2xl shadow-sm border border-gray-100 max-w-4xl mx-auto animate-fadeIn">
      <h2 className="text-xl font-serif font-bold text-[#0A1A2F] uppercase border-l-4 border-[#C9A03D] pl-3 mb-6">
        CREATE NEW LUXURY LISTING
      </h2>
      <form onSubmit={handleFormSubmit} className="space-y-6 text-sm">
        
        {/* Title & Type */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 flex flex-col space-y-2">
            <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Property Title</label>
            <input required type="text" name="title" value={formData.title || ""} onChange={handleInputChange} placeholder="e.g., Royal Sea penthouse" className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition" />
          </div>
          <div className="flex flex-col space-y-2">
            <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Property Type</label>
            <select name="property_type" value={formData.property_type || "apartment"} onChange={handleInputChange} className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition">
              <option value="apartment">Apartment</option>
              <option value="villa">Villa</option>
              <option value="penthouse">Penthouse</option>
              <option value="commercial">Commercial</option>
            </select>
          </div>
        </div>

        {/* Specs: Price, Beds, Baths, Area */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="flex flex-col space-y-2">
            <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Price ($)</label>
            <input required type="number" name="price" value={formData.price || ""} onChange={handleInputChange} className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition" />
          </div>
          <div className="flex flex-col space-y-2">
            <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Bedrooms</label>
            <input type="number" name="bedrooms" value={formData.bedrooms || ""} onChange={handleInputChange} className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition" />
          </div>
          <div className="flex flex-col space-y-2">
            <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Bathrooms</label>
            <input type="number" name="bathrooms" value={formData.bathrooms || ""} onChange={handleInputChange} className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition" />
          </div>
          <div className="flex flex-col space-y-2">
            <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Area (Sq-Ft)</label>
            <input type="number" name="area_sqft" value={formData.area_sqft || ""} onChange={handleInputChange} className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition" />
          </div>
        </div>

        {/* Address */}
        <div className="flex flex-col space-y-2">
          <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Address Location</label>
          <input required type="text" name="address" value={formData.address || ""} onChange={handleInputChange} placeholder="e.g., Prime Sector, Downtown" className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition" />
        </div>

        {/* Description Field */}
        <div className="flex flex-col space-y-2">
          <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Property Description</label>
          <textarea name="description" rows="4" value={formData.description || ""} onChange={handleInputChange} placeholder="Write high-end alluring details about this asset..." className="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl focus:border-[#C9A03D] outline-none transition resize-none" />
        </div>

        {/* IMAGE UPLOADER */}
        <div className="flex flex-col space-y-3">
          <label className="font-bold uppercase text-xs text-[#0A1A2F]/70">Upload Property Images</label>
          <div className="border-2 border-dashed border-gray-200 bg-gray-50 rounded-2xl p-6 text-center relative hover:border-[#C9A03D] transition">
            <input type="file" multiple accept="image/*" onChange={handleImageChange} className="absolute inset-0 opacity-0 cursor-pointer" />
            <p className="text-xs font-bold text-gray-500 uppercase">Click or Drag to browse images</p>
          </div>
          {propertyImages.length > 0 && (
            <div className="grid grid-cols-4 gap-4 p-2 bg-gray-50 rounded-xl">
              {propertyImages.map((img, i) => (
                <div key={i} className="relative h-20 rounded-lg overflow-hidden border">
                  <img src={img.preview} alt="preview" className="w-full h-full object-cover" />
                  <button type="button" onClick={() => removeImage(i)} className="absolute top-1 right-1 bg-red-500 text-white text-[10px] rounded-full h-4 w-4 flex items-center justify-center cursor-pointer shadow-md">✕</button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Submit Button */}
        <button type="submit" className="w-full h-12 bg-[#0A1A2F] text-white hover:bg-[#C9A03D] hover:text-[#0A1A2F] font-bold text-xs rounded-xl uppercase transition cursor-pointer tracking-wider shadow-md">
          Publish Luxury Asset ➔
        </button>
      </form>
    </div>
  );
};

export default AddProperty;