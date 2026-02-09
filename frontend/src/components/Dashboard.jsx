import React from 'react';

const Dashboard = ({ meta }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card title="Total Players" value={meta.total_players} color="from-blue-500 to-cyan-500" />
      <Card title="Total Goals" value={meta.total_goals.toLocaleString()} color="from-emerald-500 to-green-500" />
      <Card title="Avg xG per 90" value={meta.avg_xg} color="from-purple-500 to-pink-500" />
    </div>
  );
};

const Card = ({ title, value, color }) => (
  <div className="glass p-6 rounded-2xl relative overflow-hidden group">
    <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${color} opacity-10 rounded-full blur-2xl -mr-16 -mt-16 group-hover:opacity-20 transition-opacity duration-500`}></div>
    <h3 className="text-slate-400 text-sm font-medium uppercase tracking-wider">{title}</h3>
    <p className="text-4xl font-bold mt-2 text-white">{value}</p>
  </div>
);

export default Dashboard;