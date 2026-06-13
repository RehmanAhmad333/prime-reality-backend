import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const SavedProperties = () => {
  const [savedList, setSavedList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [actionLoading, setActionLoading] = useState(null);

  const fetchWishlist = async () => {
    setLoading(true);
    try {
      // ✅ Fixed according to Section 4: GET /api/v1/saved
      const response = await api.get('/saved');
      setSavedList(response.data || []);
      setErrorMsg('');
    } catch (err) {
      setErrorMsg(err?.response?.data?.detail || 'Wishlist load karne mein masla hua.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  const handleRemove = async (propertyId) => {
    setActionLoading(propertyId);
    try {
      // ✅ Fixed according to Section 4: DELETE /api/v1/saved/{property_id}
      await api.delete(`/saved/${propertyId}`);
      setSavedList((prevList) => prevList.filter(item => (item.id || item._id || item) !== propertyId));
      setErrorMsg('');
    } catch (err) {
      setErrorMsg(err?.response?.data?.detail || 'Property ko remove nahi kiya ja saka.');
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-100 pb-4">
        <h3 className="text-xl font-serif font-bold text-[#0A1A2F] uppercase border-l-4 border-[#C9A03D] pl-3">Saved Luxury Wishlist</h3>
        <p className="text-gray-400 text-xs font-semibold uppercase mt-1">Your curated selection of top high-end listings</p>
      </div>

      {errorMsg && <div className="p-4 bg-red-100 text-red-700 font-bold text-xs rounded-xl border border-red-200">⚠️ {errorMsg}</div>}

      {loading ? (
        <div className="text-center py-10 text-sm font-semibold text-[#C9A03D] animate-pulse">🔄 Contacting Backend API Pipeline...</div>
      ) : savedList.length === 0 ? (
        <p className="text-sm text-gray-400 italic bg-gray-50 p-6 rounded-2xl text-center border border-dashed border-gray-200">Aapki wishlist abhi khali hai.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {savedList.map((item) => {
            // Backend dynamic key format validation
            const propertyId = typeof item === 'object' ? (item.property_id || item.id || item._id) : item;
            return (
              <div key={propertyId} className="bg-white border border-gray-100 rounded-2xl p-5 flex justify-between items-center shadow-sm">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-[#0A1A2F]/5 rounded-xl flex items-center justify-center font-bold text-sm text-[#C9A03D]">🏢</div>
                  <div>
                    <h4 className="font-bold text-sm text-[#0A1A2F]">Property #{propertyId}</h4>
                    <p className="text-[10px] text-gray-400 uppercase font-semibold">Saved Item</p>
                  </div>
                </div>
                <button type="button" onClick={() => handleRemove(propertyId)} disabled={actionLoading === propertyId}
                  className="p-2 text-red-500 hover:bg-red-50 rounded-xl text-xs font-bold transition disabled:opacity-50">
                  {actionLoading === propertyId ? '⏳ Wait...' : '✕ Remove'}
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default SavedProperties;