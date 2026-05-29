'use client';

import { LineChart } from './charts/LineChart';
import { BarChart } from './charts/BarChart';
import { PieChart } from './charts/PieChart';
import { CardDisplay } from './charts/CardDisplay';

interface ChartDisplayProps {
  chartType: string;
  data: any[];
  fields: string[];
  temporalField: string | null;
}

export function ChartDisplay({
  chartType,
  data,
  fields,
  temporalField,
}: ChartDisplayProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-8 text-center">
        <p className="text-slate-400">No data available for visualization</p>
      </div>
    );
  }

  switch (chartType) {
    case 'line':
      return <LineChart data={data} temporalField={temporalField} />;
    case 'bar':
    case 'grouped_bar':
      return <BarChart data={data} fields={fields} />;
    case 'pie':
      return <PieChart data={data} />;
    case 'card':
      return <CardDisplay data={data} />;
    case 'horizontal_bar':
      return <BarChart data={data} fields={fields} horizontal />;
    default:
      return (
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-8">
          <p className="text-slate-400">
            Chart type &apos;{chartType}&apos; is not yet supported
          </p>
        </div>
      );
  }
}
