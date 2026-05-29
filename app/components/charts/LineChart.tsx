'use client';

import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface LineChartProps {
  data: any[];
  temporalField?: string | null;
}

export function LineChart({ data, temporalField }: LineChartProps) {
  if (!data || data.length === 0) {
    return <div className="text-slate-400">No data to display</div>;
  }

  const xAxisKey = temporalField || 'year';
  
  // Determine which columns are numeric
  let numericColumns = data.length > 0
    ? Object.keys(data[0]).filter(
        key =>
          key !== xAxisKey &&
          typeof data[0][key] === 'number'
      )
    : ['value'];

  // Ensure we have numeric columns
  if (numericColumns.length === 0) {
    return <div className="text-slate-400">No numeric data to display</div>;
  }

  // Clean data: replace NaN values with 0
  const cleanedData = data.map(row => {
    const cleanedRow: any = { ...row };
    numericColumns.forEach(col => {
      const val = row[col];
      const numVal = Number(val);
      cleanedRow[col] = isNaN(numVal) || !isFinite(numVal) ? 0 : numVal;
    });
    return cleanedRow;
  });

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Trend Analysis</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RechartsLineChart data={cleanedData} margin={{ top: 20, right: 20, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey={xAxisKey} stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
            }}
            labelStyle={{ color: '#e2e8f0' }}
          />
          <Legend />
          {numericColumns.map((column, index) => (
            <Line
              key={column}
              type="monotone"
              dataKey={column}
              stroke={getColor(index)}
              strokeWidth={2}
              dot={{ fill: getColor(index), r: 4 }}
              isAnimationActive={false}
            />
          ))}
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  );
}

function getColor(index: number): string {
  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
  return colors[index % colors.length];
}
