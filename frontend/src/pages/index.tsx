'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Select from 'react-select';

const CandlestickChart = dynamic(() => import('../components/CandlestickChart'), {
  ssr: false,
});

// Country options list
const countryOptions = [
  'Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Bosnia', 'Botswana',
  'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus',
  'Czech Republic', 'Denmark', 'Dubai', 'Egypt', 'Finland', 'France', 'Germany', 'Greece',
  'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy',
  'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Lebanon',
  'Luxembourg', 'Malawi', 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro',
  'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan',
  'Palestine', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
  'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea',
  'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Tanzania', 'Thailand', 'Tunisia',
  'Turkey', 'Uganda', 'Ukraine', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela',
  'Vietnam', 'Zambia', 'Zimbabwe',
].map((c) => ({ label: c, value: c.toLowerCase() }));

// Asset Class List
const assetOptions = [
  { label: 'Stocks', value: 'stocks' },
  { label: 'Funds', value: 'funds' },
  { label: 'ETFs', value: 'etfs' },
  { label: 'Cryptocurrency', value: 'cryptocurrency' },
];

export default function Home() {
  const [candles, setCandles] = useState([]);
  const [ticker, setTicker] = useState('');
  const [availableTickers, setAvailableTickers] = useState([]);
  const [type, setType] = useState('stocks');
  const [country, setCountry] = useState('united states');
  const [from, setFrom] = useState(() => {
    const d = new Date();
    d.setFullYear(d.getFullYear() - 1);
    return d.toISOString().slice(0, 10);
  });
  const [to, setTo] = useState(() => new Date().toISOString().slice(0, 10));
  const [interval, setInterval] = useState('daily');
  const [loading, setLoading] = useState(false);

  const fetchCandles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        type,
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

  // Fetch tickers on assetType or country change
  useEffect(() => {
    const fetchTickers = async () => {
      if (!type) return;
      let endpoint = '';
      switch (type) {
        case 'stocks': endpoint = 'get_stocks'; break;
        case 'funds': endpoint = 'get_funds'; break;
        case 'etfs': endpoint = 'get_etfs'; break;
        case 'cryptocurrency': endpoint = 'get_cryptos'; break;
      }

      const url =
        type === 'cryptocurrency'
          ? `http://127.0.0.1:8000/v01/${endpoint}`
          : `http://127.0.0.1:8000/v01/${endpoint}?country=${encodeURIComponent(country)}`;

      try {
        const res = await fetch(url);
        const data = await res.json();
        const list = data.available_stocks || data.available_funds || data.available_etfs || data.available_cryptos || [];
        setAvailableTickers(list);
        if (list.length > 0) setTicker(list[0].ticker);
        else setTicker('');
      } catch (err) {
        console.error(err);
        setAvailableTickers([]);
      }
    };

    fetchTickers();
  }, [type, country]);

  useEffect(() => {
    fetchCandles();
  }, [ticker]);

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
            {/* Asset Type */}
            <div>
              <label className="block text-sm font-medium mb-1">Asset Type</label>
              <Select
                options={assetOptions}
                value={assetOptions.find((opt) => opt.value === type)}
                onChange={(sel) => setType(sel?.value || '')}
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

            {/* Ticker */}
            <div>
              <label className="block text-sm font-medium mb-1">Ticker</label>
              <select
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              >
                {availableTickers.map(({ stock, ticker }) => (
                  <option key={ticker} value={ticker}>
                    {stock} ({ticker})
                  </option>
                ))}
              </select>
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
