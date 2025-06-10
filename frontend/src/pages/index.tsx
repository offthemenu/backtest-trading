'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Select from 'react-select';

const CandlestickChart = dynamic(() => import('../components/CandlestickChart'), {
  ssr: false,
});

// Country options list
const countryOptions = [
  'argentina', 'australia', 'austria', 'bahrain', 'bangladesh', 'belgium', 'bosnia', 'botswana',
  'brazil', 'bulgaria', 'canada', 'chile', 'china', 'colombia', 'costa rica', 'croatia', 'cyprus',
  'czech republic', 'denmark', 'dubai', 'egypt', 'finland', 'france', 'germany', 'greece',
  'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iraq', 'ireland', 'israel', 'italy',
  'ivory coast', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kuwait', 'lebanon',
  'luxembourg', 'malawi', 'malaysia', 'malta', 'mauritius', 'mexico', 'mongolia', 'montenegro',
  'morocco', 'namibia', 'netherlands', 'new zealand', 'nigeria', 'norway', 'oman', 'pakistan',
  'palestine', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda',
  'saudi arabia', 'serbia', 'singapore', 'slovakia', 'slovenia', 'south africa', 'south korea',
  'spain', 'sri lanka', 'sweden', 'switzerland', 'taiwan', 'tanzania', 'thailand', 'tunisia',
  'turkey', 'uganda', 'ukraine', 'united kingdom', 'united states', 'uruguay', 'venezuela',
  'vietnam', 'zambia', 'zimbabwe',
].map((c) => ({ label: c.charAt(0).toUpperCase() + c.slice(1), value: c }));

export default function Home() {
  const [candles, setCandles] = useState([]);
  const [ticker, setTicker] = useState('TSLA');
  const [country, setCountry] = useState('united states');
  const [from, setFrom] = useState('2023-01-01');
  const [to, setTo] = useState('2023-12-31');
  const [interval, setInterval] = useState('daily');
  const [loading, setLoading] = useState(false);

  const fetchCandles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        ticker,
        country,
        from,
        to,
        interval,
      });

      const response = await fetch(`http://127.0.0.1:8000/v01/load_data?${params.toString()}`);
      const data = await response.json();
      if (response.ok) {
        setCandles(data.candles);
      } else {
        console.error('Server error:', data.detail);
        setCandles([]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setCandles([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandles(); // initial load
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCandles();
  };

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-1/4 bg-gray-200 p-4">
          <h2 className="text-xl font-bold mb-4">Chart Settings</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Ticker */}
            <div>
              <label htmlFor="ticker" className="block text-sm font-medium mb-1">Ticker</label>
                <input
                type="text"
                id="ticker"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                className="w-full p-2 border border-gray-300 rounded"
                placeholder="Enter ticker (e.g. TSLA)"
                autoComplete="off"
                />
            </div>

            {/* Country */}
            <div>
              <label htmlFor="country" className="block text-sm font-medium mb-1">Country</label>
              <Select
                id="country"
                options={countryOptions}
                value={countryOptions.find(option => option.value === country)}
                onChange={(selected) => setCountry(selected?.value || '')}
                className="text-sm"
              />
            </div>

            {/* From Date */}
            <div>
              <label htmlFor="from" className="block text-sm font-medium mb-1">From Date</label>
              <input
                type="date"
                id="from"
                value={from}
                onChange={(e) => setFrom(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>

            {/* To Date */}
            <div>
              <label htmlFor="to" className="block text-sm font-medium mb-1">To Date</label>
              <input
                type="date"
                id="to"
                value={to}
                onChange={(e) => setTo(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>

            {/* Interval */}
            <div>
              <label htmlFor="interval" className="block text-sm font-medium mb-1">Interval</label>
              <select
                id="interval"
                value={interval}
                onChange={(e) => setInterval(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>

            {/* Submit */}
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            >
              Load Chart
            </button>
          </form>
        </aside>

        {/* Chart */}
        <main className="flex-1 p-4 bg-white">
          <h2 className="text-xl font-bold mb-4">Chart Area</h2>
          {loading ? (
            <div>Loading...</div>
          ) : (
            <CandlestickChart candles={candles} ticker={ticker} />
          )}
        </main>
      </div>

      {/* Bottom Panel */}
      <footer className="bg-gray-100 p-4">
        <h2 className="text-xl font-bold mb-2">Trade Log</h2>
        {/* Future: Trade Log Table */}
      </footer>
    </div>
  );
}
