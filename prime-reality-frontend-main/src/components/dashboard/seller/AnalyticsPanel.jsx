import React, { useState, useEffect } from 'react';
import api from "../../../services/api";

const AnalyticsPanel = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        // 🟢 FIXED ENDPOINT: API list ke Section 9 ke mutabiq platform statistics fetch kar rahe hain
        const response = await api.get('/platform/stats');
        setStats(response?.data);
        setErrorMsg('');
      } catch (err) {
        console.error("Analytics Error:", err);
        setErrorMsg('Failed to fetch real-time pipeline metrics.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  return (
    <div className="space-y-4">
      <div className="border-b border-gray-100 pb-4">
        <h3 className="text-xl font-serif font-bold text-[#0A1A2F]">SALES ANALYTICS ENGINE</h3>
        <p className="text-xs text-gray-400 font-semibold uppercase mt-0.5">Statistical insights, revenue charts, and conversion funnels</p>
      </div>

      {/* Error state handler wrapper */}
      {errorMsg && (
        <div className="p-3 text-xs font-bold text-red-600 bg-red-50 border border-red-200 rounded-xl">
          ⚠️ {errorMsg}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Total Properties Grid Block */}
        <div className="p-5 bg-gray-50 rounded-2xl border border-gray-100 relative">
          <span className="text-[10px] uppercase font-bold text-gray-400">Total Properties Cataloged</span>
          <div className="text-2xl font-bold text-[#0A1A2F] mt-1">
            {loading ? (
              <span className="text-sm font-normal text-gray-300 animate-pulse">Syncing...</span>
            ) : (
              `${stats?.total_properties || 0} Assets`
            )}
          </div>
        </div>

        {/* Visit Multiplier Grid Block */}
        <div className="p-5 bg-gray-50 rounded-2xl border border-gray-100">
          <span className="text-[10px] uppercase font-bold text-gray-400">Conversion Multiplier</span>
          <div className="text-2xl font-bold text-[#C9A03D] mt-1">
            {loading ? (
              <span className="text-sm font-normal text-gray-300 animate-pulse">Calculating...</span>
            ) : (
              `${stats?.visit_multiplier || '12'}X`
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPanel;