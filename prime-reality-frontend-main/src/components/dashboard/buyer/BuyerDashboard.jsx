import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// ALIGNED IMPORT: Syncing with Prinkle's global api layer
import api from '../../../services/api'; 
import SavedProperties from './SavedProperties';
import ScheduleViewing from './ScheduleViewing';
import SearchHistory from './SearchHistory';
import { clearAuthData } from '../../../utils/helpers/authHelper';

// Buyer Dashboard Component
// Manages real estate inquiries, wishlist management, and property logs.
const BuyerDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('my-inquiries');
  const [myInquiries, setMyInquiries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Fetch submitted inquiries from repository layer safely
  const fetchMyInquiries = async () => {
    setLoading(true);
    try {
      const response = await api.get('/inquiries');
      
      // CRASH FIX: Object wrapping and data payload parsing safely
      const data = response?.data;
      if (Array.isArray(data)) {
        setMyInquiries(data);
      } else if (data && Array.isArray(data.inquiries)) {
        setMyInquiries(data.inquiries);
      } else if (data && Array.isArray(data.data)) {
        setMyInquiries(data.data);
      } else {
        setMyInquiries([]);
      }
      setErrorMsg('');
    } catch (err) {
      setErrorMsg(
        err?.response?.data?.detail || 'Failed to load your inquiries record ledger.'
      );
    } finally {
      setLoading(false);
    }
  };

  // Sync effect context based on active layout panel
  useEffect(() => {
    if (activeTab === 'my-inquiries') {
      fetchMyInquiries();
    }
  }, [activeTab]);

  // Handle centralized state logout trigger
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
              onClick={() => setActiveTab('my-inquiries')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'my-inquiries' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>💌</span> <span>My Inquiries Track</span>
            </button>

            <button 
              type="button" 
              onClick={() => setActiveTab('saved-properties')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'saved-properties' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>⭐</span> <span>Saved Wishlist</span>
            </button>

            <button 
              type="button" 
              onClick={() => setActiveTab('schedules')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'schedules' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>📅</span> <span>Viewing Schedules</span>
            </button>

            <button 
              type="button" 
              onClick={() => setActiveTab('history')} 
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${
                activeTab === 'history' ? 'bg-[#C9A03D]/20 text-[#C9A03D]' : 'hover:bg-white/5 text-gray-300'
              }`}
            >
              <span>🔍</span> <span>Search Logs</span>
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
          <div className="text-gray-400 tracking-widest uppercase text-[10px] text-center">Buyer Hub</div>
        </div>
      </div>

      {/* DYNAMIC METRICS AND DASHBOARD VIEWPORT */}
      <div className="flex-grow p-6 md:p-10 overflow-y-auto h-screen">
        {/* API Notifications */}
        {errorMsg && (
          <div className="mb-6 p-4 bg-red-100 text-red-700 font-bold text-xs rounded-xl border border-red-200">
            ⚠️ {errorMsg}
          </div>
        )}

        {loading && (
          <div className="text-sm font-semibold text-[#C9A03D] mb-4 animate-pulse">
            🔄 Contacting Prime Reality Backend API Pipeline...
          </div>
        )}

        {/* TAB 1: SUBMITTED CLIENT INQUIRIES */}
        {activeTab === 'my-inquiries' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6">
            <div className="border-b border-gray-100 pb-4">
              <h2 className="text-2xl font-serif font-bold uppercase border-l-4 border-[#C9A03D] pl-3">My Inquiries Track</h2>
              <p className="text-gray-400 text-xs font-semibold uppercase mt-1">Live updates on responses from estate owners</p>
            </div>

            <div className="space-y-4">
              {myInquiries.length === 0 && !loading ? (
                <div className="p-6 text-center text-gray-400 text-xs font-medium">You haven't sent any inquiries yet.</div>
              ) : (
                myInquiries.map((inq) => (
                  <div key={inq.id || inq._id} className="p-5 bg-gray-50 rounded-2xl border border-gray-100 space-y-2.5 hover:shadow-sm transition">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-bold text-sm text-[#0A1A2F]">
                          {inq.property_title || inq.property?.title || `Property ID: ${inq.property_id || inq.propertyId}`}
                        </h4>
                        <p className="text-[10px] text-gray-400 uppercase font-bold mt-0.5">Inquiry ID: {inq.id || inq._id}</p>
                      </div>
                      <span className="px-2.5 py-1 rounded-full text-[9px] font-bold uppercase bg-amber-50 text-amber-600 border border-amber-200">
                        {inq.status || 'Active'}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 italic bg-white p-3 rounded-xl border border-gray-100 shadow-inner">
                      "Message: {inq.message || 'No custom message sent.'}"
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* RELATED DYNAMIC LAYOUTS */}
        {activeTab === 'saved-properties' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
            <SavedProperties />
          </div>
        )}

        {activeTab === 'schedules' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
            <ScheduleViewing />
          </div>
        )}

        {activeTab === 'history' && (
          <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-gray-100">
            <SearchHistory />
          </div>
        )}
      </div>
    </div>
  );
};

export default BuyerDashboard;