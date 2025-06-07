export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        <aside className="w-1/4 bg-gray-200 p-4">
          <h2 className="text-xl font-bold mb-4">Settings</h2>
          {/* Future: Ticker Info + RSI/EMA Settings */}
        </aside>
        <main className="flex-1 p-4 bg-white">
          <h2 className="text-xl font-bold mb-4">Chart Area</h2>
          {/* Future: Plotly.js Charts */}
        </main>
      </div>
      <footer className="bg-gray-100 p-4">
        <h2 className="text-xl font-bold mb-2">Trade Log</h2>
        {/* Future: Trade Log Table */}
      </footer>
    </div>
  );
}