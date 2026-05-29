'use client';

import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface BarChartProps {
  data: any[];
  fields: string[];
  horizontal?: boolean;
}

export function BarChart({ data, fields, horizontal }: BarChartProps) {
  if (!data || data.length === 0) {
    return <div className="text-slate-400">No data to display</div>;
  }

  // Determine categorical and numeric columns
  const categoricalFields = fields.filter(
    f => data.length > 0 && typeof data[0][f] === 'string'
  );
  const xAxisKey = categoricalFields[0] || 'country';
  let numericColumns = fields.filter(f => f !== xAxisKey);
  
  // If no numeric columns found in fields, find them from data
  if (numericColumns.length === 0 && data.length > 0) {
    numericColumns = Object.keys(data[0]).filter(
      key => key !== xAxisKey && typeof data[0][key] === 'number'
    );
  }

  // If still no numeric columns, show error
  if (numericColumns.length === 0) {
    return <div className="text-slate-400">No numeric data to display</div>;
  }

  // Clean data: replace NaN values with 0
  const cleanedData = data.map(row => {
    const cleanedRow: any = { ...row };
    // Clean all numeric columns
    numericColumns.forEach(col => {
      const val = row[col];
      const numVal = Number(val);
      cleanedRow[col] = isNaN(numVal) || !isFinite(numVal) ? 0 : numVal;
    });
    return cleanedRow;
  });

  const chartMargin = horizontal
    ? { left: 100, right: 20, top: 20, bottom: 20 }
    : { bottom: 60, left: 80, right: 20, top: 20 };

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Comparison</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RechartsBarChart
          data={cleanedData}
          layout={horizontal ? 'vertical' : 'horizontal'}
          margin={chartMargin}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          {!horizontal && (
            <XAxis 
              type="category" 
              dataKey={xAxisKey} 
              stroke="#94a3b8" 
              angle={-45}
              textAnchor="end"
              height={80}
            />
          )}
          {horizontal && (
            <XAxis 
              type="number" 
              stroke="#94a3b8"
            />
          )}
          {!horizontal && (
            <YAxis
              type="number"
              stroke="#94a3b8"
              width={80}
            />
          )}
          {horizontal && (
            <YAxis 
              type="category" 
              dataKey={xAxisKey} 
              stroke="#94a3b8" 
              width={100}
            />
          )}
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
            <Bar
              key={column}
              dataKey={column}
              fill={getColor(index)}
              radius={[8, 8, 0, 0]}
              isAnimationActive={false}
            />
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}

function getColor(index: number): string {
  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
  return colors[index % colors.length];
}
