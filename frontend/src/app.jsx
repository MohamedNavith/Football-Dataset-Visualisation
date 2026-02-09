import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Users, Trophy, Search } from 'lucide-react';
import Dashboard from './components/Dashboard';
import PlayerTable from './components/PlayerTable';
import Charts from './components/Charts';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [data, setData] = useState(null);
  const [filters, setFilters] = useState({ league: 'All', search: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [filters]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const query = new URLSearchParams(filters).toString();
      const res = await fetch(`http://localhost:5000/api/stats?${query}`);
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-dark text-slate-200 selection:bg-accent selection:text-white flex">
      {/* Sidebar */}
      <nav className="fixed left-0 top-0 h-full w-20 flex flex-col items-center py-8 glass z-50">
        <div className="mb-12 text-accent p-2 rounded-full bg-accent/10"><Trophy size={28} /></div>
        <NavIcon icon={<LayoutDashboard />} active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
        <NavIcon icon={<Users />} active={activeTab === 'players'} onClick={() => setActiveTab('players')} />
      </nav>

      {/* Main Content */}
      <main className="pl-20 w-full">
        <header className="p-8 pb-0 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              Football Analytics Pro
            </h1>
            <p className="text-slate-400 mt-2">Season 2014-2020 Data Explorer</p>
          </div>

          <div className="flex gap-4">
            <select 
              className="glass px-4 py-2 rounded-lg outline-none focus:ring-2 ring-accent text-sm bg-transparent"
              value={filters.league}
              onChange={(e) => setFilters({...filters, league: e.target.value})}
            >
              <option value="All" className="bg-dark">All Leagues</option>
              <option value="EPL" className="bg-dark">Premier League</option>
              <option value="LaLiga" className="bg-dark">La Liga</option>
              <option value="Bundesliga" className="bg-dark">Bundesliga</option>
            </select>
            
            <div className="relative">
              <Search className="absolute left-3 top-2.5 text-slate-500" size={18} />
              <input 
                type="text" 
                placeholder="Search player..." 
                className="glass pl-10 pr-4 py-2 rounded-lg outline-none focus:ring-2 ring-accent w-64 text-sm bg-transparent"
                onChange={(e) => setFilters({...filters, search: e.target.value})}
              />
            </div>
          </div>
        </header>

        <div className="p-8">
          {loading && !data ? (
            <div className="flex items-center justify-center h-64 text-accent animate-pulse">Loading Analytics...</div>
          ) : (
            <>
              {activeTab === 'dashboard' && data && (
                <div className="space-y-6">
                  <Dashboard meta={data.meta} />
                  <Charts data={data.charts} />
                </div>
              )}
              {activeTab === 'players' && data && (
                <PlayerTable players={data.table} />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}

const NavIcon = ({ icon, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`p-4 mb-4 rounded-xl transition-all duration-300 ${active ? 'bg-accent text-white shadow-lg shadow-blue-500/30' : 'text-slate-500 hover:bg-white/5 hover:text-white'}`}
  >
    {icon}
  </button>
);

export default App;