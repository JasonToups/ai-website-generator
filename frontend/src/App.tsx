import { Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { GalleryPage } from '@/pages/GalleryPage';
import { DashboardPage } from '@/pages/DashboardPage';
import './App.css';

function App() {
  const location = useLocation();
  const navigate = useNavigate();

  // Determine active tab based on current route
  const getActiveTab = () => {
    if (location.pathname === '/gallery') return 'gallery';
    return 'dashboard';
  };

  const activeTab = getActiveTab();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI Website Generator</h1>
              <p className="text-gray-600">
                Powered by CrewAI - Let our team of AI agents build your website
              </p>
            </div>
          </div>

          {/* Tab Navigation - Dashboard first, Gallery second */}
          <div className="flex space-x-8">
            <button
              onClick={() => navigate('/dashboard')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'dashboard'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}>
              🏠 Dashboard
            </button>
            <button
              onClick={() => navigate('/gallery')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'gallery'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}>
              🖼️ Gallery
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/gallery" element={<GalleryPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
