import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../../services/api';
import MyPropertiesList from './MyPropertiesList'; 
import PropertyInquiries from './PropertyInquiries';
import AnalyticsPanel from './AnalyticsPanel';
import AddPropertyContainer from './AddPropertyContainer';
import { clearAuthData } from '../../../utils/helpers/authHelper';

// Seller Dashboard Component
const SellerDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('my-properties');
  const [myProperties, setMyProperties] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

// Fetch listed properties safely
// backend pe /properties/my-properties route nahi hai
// is liye common /properties endpoint se seller data load kar rahe hain

const fetchMyProperties = async () => {
  setLoading(true);

  try {
    const response = await api.get("/properties");

    const data = response?.data;

    if (Array.isArray(data)) {
      setMyProperties(data);
    } else if (data && Array.isArray(data.properties)) {
      setMyProperties(data.properties);
    } else if (data && Array.isArray(data.data)) {
      setMyProperties(data.data);
    } else {
      setMyProperties([]);
    }

    setErrorMsg("");
  } catch (err) {
    console.error("Backend Error Response:", err?.response?.data);

    const rawDetail = err?.response?.data?.detail;

    if (typeof rawDetail === "string") {
      setErrorMsg(rawDetail);
    } else if (Array.isArray(rawDetail) && rawDetail[0]?.msg) {
      setErrorMsg(`${rawDetail[0].loc.join(".")} - ${rawDetail[0].msg}`);
    } else if (rawDetail && typeof rawDetail === "object") {
      setErrorMsg(JSON.stringify(rawDetail));
    } else {
      setErrorMsg("Failed to load your property catalog.");
    }
  } finally {
    setLoading(false);
  }
};
  useEffect(() => {
    if (activeTab === 'my-properties') {
      fetchMyProperties();
    }
  }, [activeTab]);

  const handleLogout = () => {
    clearAuthData();
    navigate('/login');
  };

  return (
    <div className="w-full min-h-screen bg-[#F4F6F9] text-[#0A1A2F] flex overflow-x-hidden overflow-y-auto">
      {/* SIDEBAR NAVIGATION PANEL */}
      <div className="w-64 bg-[#0A1A2F] text-white flex flex-col justify-between hidden md:flex shrink-0 shadow-xl z-10">
        <div className="p-6">
          <div className="text-xl font-serif font-bold tracking-[0.2em] text-[#C9A03D] uppercase border-b border-gray-800 pb-4">
            PRIME REALITY
          </div>

          <nav className="mt-8 space-y-2">
            <button 
              type="button" 
              onClick={() => setActiveTab('my-properties')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'my-properties' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>🏡</span> <span>My Properties</span>
            </button>

            {/* 🟢 Sidebar Add Property Button Linked Properly */}
            <button 
              type="button" 
              onClick={() => setActiveTab('add-property')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'add-property' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>✨</span> <span>Add Luxury Property</span>
            </button>

            <button 
              type="button" 
              onClick={() => setActiveTab('inquiries')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'inquiries' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>📬</span> <span>Client Inquiries</span>
            </button>

            <button 
              type="button" 
              onClick={() => setActiveTab('analytics')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'analytics' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>📈</span> <span>Sales Analytics</span>
            </button>
          </nav>
        </div>

        <div className="p-6 border-t border-gray-800 space-y-4">
          <button 
            type="button" 
            onClick={handleLogout} 
            className="w-full bg-red-600/20 text-red-400 hover:bg-red-600 hover:text-white px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition flex items-center justify-center space-x-2"
          >
            <span>🚪</span> <span>Logout Hub</span>
          </button>
          <div className="text-gray-400 tracking-widest uppercase text-[10px] text-center">Seller Hub</div>
        </div>
      </div>

      {/* DASHBOARD VIEWPORT AREA */}
      <div className="flex-grow p-6 md:p-10 overflow-y-auto h-screen">
        {errorMsg && (
          <div className="mb-6 p-4 bg-red-100 text-red-700 font-bold text-xs rounded-xl border border-red-200">
            ⚠️ {errorMsg}
          </div>
        )}

        {loading && (
          <div className="text-sm font-semibold text-[#C9A03D] mb-4 animate-pulse">
            🔄 Syncing metrics via Prime Reality Backend API Pipeline...
          </div>
        )}

        {/* TAB 1: PROPERTIES CATALOGUE LIST */}
        {activeTab === 'my-properties' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
            <MyPropertiesList properties={myProperties} refreshList={fetchMyProperties} />
          </div>
        )}

        {/* 🟢 TAB 2: SEPARATE ADD PROPERTY CONTENT VIEW */}
        {activeTab === 'add-property' && (
          <AddPropertyContainer 
            onPropertyAdded={() => {
              fetchMyProperties(); 
              setActiveTab('my-properties'); // Form submit hone ke baad auto list par bhej dega
            }} 
          />
        )}

        {/* RELATED SYSTEM VIEWS */}
        {activeTab === 'inquiries' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
            <PropertyInquiries />
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
            <AnalyticsPanel />
          </div>
        )}
      </div>
    </div>
  );
};

export default SellerDashboard;