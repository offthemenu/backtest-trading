'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

const CandlestickChart = dynamic(() => import('../components/CandlestickChart'), {
  ssr: false,
});

export default function Home() {
  const [candles, setCandles] = useState([]);
  const [ticker, setTicker] = useState('TSLA');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCandles = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/v01/load_data?ticker=${ticker}&from=2022-01-01`
        );
        const data = await response.json();
        setCandles(data.candles);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCandles();
  }, [ticker]);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Top section: Sidebar + Chart */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-1/4 bg-gray-200 p-4">
          <h2 className="text-xl font-bold mb-4">Settings</h2>
          <div className="mb-2">
            <label className="block text-sm font-medium mb-1" htmlFor="ticker">
              Select Ticker
            </label>
            <select
              id="ticker"
              value={ticker}
              onChange={(e) => {
                setLoading(true);
                setTicker(e.target.value);
              }}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="TSLA">TSLA</option>
              <option value="AAPL">AAPL</option>
              <option value="GOOG">GOOG</option>
              <option value="MSFT">MSFT</option>
            </select>
          </div>
        </aside>

        {/* Chart Panel */}
        <main className="flex-1 p-4 bg-white">
          <h2 className="text-xl font-bold mb-4">Chart Area</h2>
          {loading ? (
            <div>Loading...</div>
          ) : (
            <CandlestickChart candles={candles} ticker={ticker} />
          )}
        </main>
      </div>

      {/* Bottom Panel: Trade Log */}
      <footer className="bg-gray-100 p-4">
        <h2 className="text-xl font-bold mb-2">Trade Log</h2>
        {/* Future: Trade Log Table */}
      </footer>
    </div>
  );
}
