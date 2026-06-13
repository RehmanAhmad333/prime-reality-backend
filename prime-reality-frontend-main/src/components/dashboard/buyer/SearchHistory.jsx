import React from 'react';

const SearchHistory = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-100 pb-4">
        <h3 className="text-xl font-serif font-bold text-[#0A1A2F] uppercase border-l-4 border-[#C9A03D] pl-3">Recent Searches</h3>
        <p className="text-gray-400 text-xs font-semibold uppercase mt-1">Your recent search query tracks and session logs</p>
      </div>

      {/* Local Client Device Logs Fallback View */}
      <div className="p-8 text-center text-gray-400 text-xs font-medium bg-gray-50 rounded-2xl border border-dashed border-gray-200">
        Aapke current session ki live search tracking active hai. Browser history cached listings clear hain!
      </div>
    </div>
  );
};

export default SearchHistory;