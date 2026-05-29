'use client';

import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  Legend,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface PieChartProps {
  data: any[];
}

export function PieChart({ data }: PieChartProps) {
  if (!data || data.length === 0) {
    return <div className="text-slate-400">No data to display</div>;
  }

  // Use first string column as name and first numeric column as value
  const nameKey = Object.keys(data[0]).find(k => typeof data[0][k] === 'string') || 'name';
  const valueKey = Object.keys(data[0]).find(k => typeof data[0][k] === 'number') || 'value';

  // Clean data: replace NaN values with 0
  const chartData = data.map((d: any) => {
    const value = Number(d[valueKey]);
    return {
      name: d[nameKey],
      value: isNaN(value) ? 0 : value,
    };
  });

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RechartsPieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={getColor(index)} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
            }}
            labelStyle={{ color: '#e2e8f0' }}
          />
          <Legend />
        </RechartsPieChart>
      </ResponsiveContainer>
    </div>
  );
}

function getColor(index: number): string {
  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
  return colors[index % colors.length];
}
