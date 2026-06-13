import React, { useState } from "react";
import api from "../../../services/api";
import AddProperty from "./AddProperty.jsx";

const AddPropertyContainer = ({ onPropertyAdded }) => {
  // 1. Unified Form State matching DB validation
  const [formData, setFormData] = useState({
    title: "",
    property_type: "apartment",
    price: "",
    bedrooms: "",
    bathrooms: "",
    area_sqft: "",
    address: "",
    description: "",
  });

  // 2. Local Images State (holds file object and preview URL)
  const [propertyImages, setPropertyImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState({ type: "", text: "" });

  // 3. Input Change Handler
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // 4. Image Picker and Preview Generator Handler
  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    
    const validImages = files.map((file) => ({
      fileObject: file,
      preview: URL.createObjectURL(file),
    }));

    setPropertyImages((prev) => [...prev, ...validImages]);
  };

  // 5. Remove Selected Image Preview Handler
  const removeImage = (index) => {
    setPropertyImages((prev) => {
      const updated = [...prev];
      // Memory leak se bachne ke liye object URL revoke karna zaroori hai
      URL.revokeObjectURL(updated[index].preview);
      updated.splice(index, 1);
      return updated;
    });
  };

  // 6. Submit Multipart Form Data to Backend API Engine
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatusMsg({ type: "", text: "" });

    // FormData Object initialization for handling files + text fields
    const dataToSend = new FormData();

    // Append regular text fields
    Object.keys(formData).forEach((key) => {
      dataToSend.append(key, formData[key]);
    });

    // Append image blobs
    propertyImages.forEach((img) => {
      dataToSend.append("images", img.fileObject);
    });

    try {
      // 🟢 FIXED ENDPOINT: API list ke mutabiq '/properties' par POST request bhej rahe hain
      const response = await api.post("/properties", dataToSend, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setStatusMsg({
        type: "success",
        text: "🎉 Luxury asset published successfully and queued for admin verification!",
      });

      // Reset Form Inputs
      setFormData({
        title: "",
        property_type: "apartment",
        price: "",
        bedrooms: "",
        bathrooms: "",
        area_sqft: "",
        address: "",
        description: "",
      });
      setPropertyImages([]);

      // Trigger automatic list refresh on the dashboard if callback exists
      if (typeof onPropertyAdded === "function") {
        onPropertyAdded();
      }
    } catch (err) {
      // FastAPI arrays validation errors ko safely capture karne ke liye string check
      const rawDetail = err?.response?.data?.detail;
      let incomingError = "Failed to publish the luxury asset listing.";
      
      if (typeof rawDetail === "string") {
        incomingError = rawDetail;
      } else if (Array.isArray(rawDetail)) {
        incomingError = rawDetail.map(e => `${e.loc.join('.')}: ${e.msg}`).join(' | ');
      }

      setStatusMsg({
        type: "error",
        text: incomingError,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4 w-full">
      {/* Dynamic Status Notifications */}
      {statusMsg.text && (
        <div
          className={`p-4 rounded-xl font-bold text-xs max-w-4xl mx-auto border ${
            statusMsg.type === "success"
              ? "bg-emerald-50 text-emerald-700 border-emerald-200"
              : "bg-red-50 text-red-700 border-red-200"
          }`}
        >
          {statusMsg.type === "success" ? "✓" : "⚠️"} {statusMsg.text}
        </div>
      )}

      {/* Loading overlay notification layer */}
      {loading && (
        <div className="text-sm font-semibold text-[#C9A03D] mb-2 animate-pulse text-center">
          ⏳ Uploading assets and registering pipeline to Prime Reality Cluster...
        </div>
      )}

      {/* Injecting your pure AddProperty presentation component */}
      <AddProperty
        formData={formData}
        handleInputChange={handleInputChange}
        handleImageChange={handleImageChange}
        propertyImages={propertyImages}
        removeImage={removeImage}
        handleFormSubmit={handleFormSubmit}
      />
    </div>
  );
};

export default AddPropertyContainer;