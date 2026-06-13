import React, { useState, useEffect } from 'react';
import api from '../../../services/api';

const ScheduleViewing = () => {
  const [viewings, setViewings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchSchedules = async () => {
    setLoading(true);
    try {
      // ✅ Fixed according to Section 6: GET /api/v1/bookings
      const response = await api.get('/bookings');
      setViewings(response.data || []);
      setErrorMsg('');
    } catch (err) {
      setErrorMsg(err?.response?.data?.detail || 'Schedules load karne mein masla hua.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-100 pb-4">
        <h3 className="text-xl font-serif font-bold text-[#0A1A2F] uppercase border-l-4 border-[#C9A03D] pl-3">Viewing Schedules</h3>
        <p className="text-gray-400 text-xs font-semibold uppercase mt-1">Track your upcoming private site tours</p>
      </div>

      {errorMsg && <div className="p-4 bg-red-100 text-red-700 font-bold text-xs rounded-xl border border-red-200">⚠️ {errorMsg}</div>}

      {loading ? (
        <div className="text-center py-10 text-sm font-semibold text-[#C9A03D] animate-pulse">🔄 Contacting Backend API Pipeline...</div>
      ) : viewings.length === 0 ? (
        <div className="p-8 text-center text-gray-400 text-xs font-medium bg-gray-50 rounded-2xl border border-dashed border-gray-200">Filhal koi viewing tour scheduled nahi hai.</div>
      ) : (
        <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
          <div className="overflow-x-auto w-full">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-100 text-[11px] font-bold text-gray-400 tracking-widest uppercase bg-gray-50">
                  <th className="py-3 px-4">Booking ID</th>
                  <th className="py-3 px-4">Property Code</th>
                  <th className="py-3 px-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 text-xs font-medium">
                {viewings.map((v) => (
                  <tr key={v.id || v._id} className="hover:bg-gray-50/50 transition">
                    <td className="py-4 px-4 font-bold text-[#0A1A2F]">#{v.id || v._id}</td>
                    <td className="py-4 px-4 text-gray-500">Property {v.property_id || 'System Managed'}</td>
                    <td className="py-4 px-4 text-center">
                      <span className={`px-2.5 py-1 rounded-full text-[9px] font-bold uppercase tracking-wider ${
                        v.status?.toLowerCase() === 'confirmed' ? 'bg-emerald-50 text-emerald-600 border border-emerald-200' : 'bg-amber-50 text-amber-600 border border-amber-200'
                      }`}>{v.status || 'pending'}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScheduleViewing;