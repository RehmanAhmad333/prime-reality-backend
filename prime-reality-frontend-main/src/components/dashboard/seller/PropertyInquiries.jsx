import React, { useState, useEffect } from 'react';
import api from "../../../services/api";

const PropertyInquiries = () => {
  const [inquiries, setInquiries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    const fetchInquiries = async () => {
      try {
        setLoading(true);
        // 🟢 FIXED ENDPOINT: API list ke Section 5 ke mutabiq client inquiries fetch kar rahe hain
        const response = await api.get('/inquiries');
        
        const data = response?.data;
        if (Array.isArray(data)) {
          setInquiries(data);
        } else if (data && Array.isArray(data.inquiries)) {
          setInquiries(data.inquiries);
        } else {
          setInquiries([]);
        }
        setErrorMsg('');
      } catch (err) {
        console.error("Inquiries Fetch Error:", err);
        setErrorMsg('Failed to establish connection with inquiry communication layer.');
      } finally {
        setLoading(false);
      }
    };

    fetchInquiries();
  }, []);

  return (
    <div className="space-y-4">
      <div className="border-b border-gray-100 pb-4">
        <h3 className="text-xl font-serif font-bold text-[#0A1A2F]">CLIENT INQUIRIES ROUTER</h3>
        <p className="text-xs text-gray-400 font-semibold uppercase mt-0.5">Direct messages and requests from potential buyers</p>
      </div>

      {/* Error state alert bar */}
      {errorMsg && (
        <div className="p-3 text-xs font-bold text-red-600 bg-red-50 border border-red-200 rounded-xl">
          ⚠️ {errorMsg}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        {loading ? (
          <div className="p-8 text-center text-sm font-semibold text-[#C9A03D] bg-gray-50 rounded-2xl border border-dashed border-gray-200 animate-pulse">
            ⏳ Synchronizing inbound communication channels from cluster...
          </div>
        ) : inquiries.length === 0 ? (
          <div className="p-8 text-center text-gray-400 text-xs font-medium bg-gray-50 rounded-2xl border border-dashed border-gray-200">
            No active buyer inquiries received on your listings yet.
          </div>
        ) : (
          inquiries.map((inq) => (
            <div 
              key={inq.id || inq._id} 
              className="p-5 bg-gray-50 rounded-2xl border border-gray-100 hover:shadow-sm transition flex flex-col md:flex-row md:justify-between md:items-start gap-4"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-[#0A1A2F]">
                    {inq.buyer_name || inq.user?.full_name || "Anonymous Buyer"}
                  </span>
                  <span className="text-[9px] text-gray-400 font-bold uppercase tracking-wider">
                    • {inq.buyer_phone || inq.user?.phone || "No Phone Contact"}
                  </span>
                </div>
                
                {/* Inquiry message text node */}
                <p className="text-xs text-gray-600 font-medium bg-white p-3 rounded-xl border border-gray-100">
                  {inq.message || "No custom text body provided by the client."}
                </p>
                
                {/* Timestamp architecture */}
                {inq.created_at && (
                  <span className="block text-[9px] text-gray-400 font-semibold uppercase pt-1">
                    Received: {new Date(inq.created_at).toLocaleString()}
                  </span>
                )}
              </div>

              {inq.property_title && (
                <div className="md:text-right self-end md:self-start shrink-0">
                  <span className="text-[9px] uppercase font-bold text-gray-400 block">Target Asset</span>
                  <span className="text-xs font-bold text-[#C9A03D]">{inq.property_title}</span>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default PropertyInquiries;