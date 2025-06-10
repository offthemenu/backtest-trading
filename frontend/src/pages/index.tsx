'use client';

import React, { useState, useEffect } from 'react';
import CandlestickChart from '../components/CandlestickChart';

export default function Home() {
  const [candles, setCandles] = useState([]);
  const [ticker, setTicker] = useState('TSLA');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCandles = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/v01/load_data?ticker=${ticker}&from=2022-01-01`);
        const data = await response.json();
        setCandles(data.candles);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchCandles();
  }, [ticker]);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      {loading ? (
        <div>Loading...</div>
      ) : (
        <CandlestickChart candles={candles} ticker={ticker} />
      )}
    </main>
  );
}

