import React from 'react';

const PlayerTable = ({ players }) => {
  return (
    <div className="glass rounded-2xl overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5 text-slate-400 text-xs uppercase tracking-wider">
              <th className="p-4 font-semibold">Player</th>
              <th className="p-4 font-semibold">Team</th>
              <th className="p-4 font-semibold">League</th>
              <th className="p-4 font-semibold text-right">Mins</th>
              <th className="p-4 font-semibold text-right text-emerald-400">Goals</th>
              <th className="p-4 font-semibold text-right text-purple-400">xG</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5 text-sm">
            {players.map((p, idx) => (
              <tr key={idx} className="hover:bg-white/5 transition-colors">
                <td className="p-4 font-medium text-white">{p.player_name}</td>
                <td className="p-4 text-slate-300">{p.team_name}</td>
                <td className="p-4"><span className="px-2 py-1 rounded text-xs font-bold bg-white/10">{p.league}</span></td>
                <td className="p-4 text-right text-slate-400">{p.minutes}</td>
                <td className="p-4 text-right font-bold text-emerald-400">{p.goals}</td>
                <td className="p-4 text-right text-purple-400">{p.xg.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PlayerTable;