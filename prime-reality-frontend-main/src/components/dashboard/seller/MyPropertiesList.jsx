import React, { useState } from 'react';
import api from "../../../services/api";

const MyPropertiesList = ({ properties, refreshList }) => {
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [localError, setLocalError] = useState('');

  // 🟢 FIXED ACTION: API list ke Section 3 ke mutabiq property hard delete trigger karna
  const handleDeleteProperty = async (propertyId) => {
    if (!window.confirm("Are you absolutely sure you want to permanently delete this property asset?")) {
      return;
    }

    try {
      setActionLoadingId(propertyId);
      setLocalError('');
      
      // Dynamic path parameters handling for deletion pipeline
      await api.delete(`/properties/${propertyId}`);
      
      // Sync local catalog state automatically with parent context registry
      if (typeof refreshList === 'function') {
        refreshList();
      }
    } catch (err) {
      console.error("Property Action Error:", err);
      const rawDetail = err?.response?.data?.detail;
      
      if (typeof rawDetail === 'string') {
        setLocalError(rawDetail);
      } else if (Array.isArray(rawDetail)) {
        setLocalError(rawDetail.map(e => `${e.loc.join('.')}: ${e.msg}`).join(' | '));
      } else {
        setLocalError('Pipeline authorization failure or deletion restricted.');
      }
    } finally {
      setActionLoadingId(null);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center border-b border-gray-100 pb-4">
        <div>
          <h3 className="text-xl font-serif font-bold text-[#0A1A2F]">MY REAL ESTATE CATALOGUE</h3>
          <p className="text-xs text-gray-400 font-semibold uppercase mt-0.5">Manage your active or pending property listings</p>
        </div>
        <button 
          type="button"
          onClick={refreshList}
          className="px-4 py-2 bg-[#0A1A2F] text-white rounded-xl text-xs font-bold uppercase tracking-wider hover:bg-opacity-90 transition"
        >
          🔄 Refresh Listings
        </button>
      </div>

      {/* Local Action Error Alerts Notification bar */}
      {localError && (
        <div className="p-3 text-xs font-bold text-red-600 bg-red-50 border border-red-200 rounded-xl">
          ⚠️ Error: {localError}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        {properties.length === 0 ? (
          <div className="p-8 text-center text-gray-400 text-xs font-medium bg-gray-50 rounded-2xl border border-dashed border-gray-200">
            No properties listed under your account yet.
          </div>
        ) : (
          properties.map((prop) => {
            const currentId = prop.id || prop._id;
            return (
              <div key={currentId} className="p-5 bg-gray-50 rounded-2xl border border-gray-100 flex justify-between items-center hover:shadow-sm transition">
                <div>
                  <h4 className="font-bold text-sm text-[#0A1A2F]">{prop.title || "Untitled Property"}</h4>
                  <p className="text-[10px] text-gray-400 uppercase font-bold mt-1">
                    ${Number(prop.price || 0).toLocaleString()}
                  </p>
                  <div className="mt-2 flex items-center gap-2">
                    {/* Status badge architecture mapping */}
                    <span className={`px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase border ${
                      prop.status === 'approved' 
                        ? 'bg-emerald-50 text-emerald-600 border-emerald-200' 
                        : prop.status === 'rejected'
                        ? 'bg-rose-50 text-rose-600 border-rose-200'
                        : 'bg-amber-50 text-amber-600 border-amber-200'
                    }`}>
                      {prop.status || 'pending'}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {/* Delete Action Trigger Interface */}
                  <button
                    type="button"
                    disabled={actionLoadingId === currentId}
                    onClick={() => handleDeleteProperty(currentId)}
                    className="px-3 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 rounded-lg text-[10px] font-bold uppercase transition disabled:opacity-50"
                  >
                    {actionLoadingId === currentId ? "⏳ ... " : "🗑️ Delete"}
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default MyPropertiesList;