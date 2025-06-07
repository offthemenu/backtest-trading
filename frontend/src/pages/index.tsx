export default function Home() {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-1/4 bg-gray-800 text-white p-4">
        Sidebar
      </div>
      
      {/* Main Content */}
      <div className="flex-1 bg-white p-4">
        Chart Area
      </div>
    </div>
  );
}
