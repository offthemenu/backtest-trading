'use client';
import dynamic from "next/dynamic";
import React from "react";
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

const CandlestickChart = ({ candles = [], ticker }) => {
    if (!Array.isArray(candles) || candles.length == 0) {
        return <div>No data available</div>;
    }
    
    const dates = candles.map(item => item.date);
    const opens = candles.map(item => item.open);
    const highs = candles.map(item => item.high);
    const lows = candles.map(item => item.low);
    const closes = candles.map(item => item.close);

    return (
        <div>
            <h2 className="text-xl font-bold mb-4">{ticker} Candlestick Chart</h2>
            <Plot
                data={[
                    {
                        x: dates,
                        open: opens,
                        high: highs,
                        low: lows,
                        close: closes,
                        type: 'candlestick',
                        xaxis: 'x',
                        yaxis: 'y'
                    }
                ]}
                layout={{
                    title: `${ticker} Stock Price`,
                    dragmode: 'zoom',
                    showlegend: false,
                    xaxis: {
                        rangeslider: { visible: false }
                    }
                }}
                style={{ width: '100%', height: '500px' }}
            />
        </div>
    );
};

export default CandlestickChart