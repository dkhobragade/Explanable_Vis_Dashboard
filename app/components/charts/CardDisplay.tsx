'use client';

interface CardDisplayProps {
  data: any[];
}

export function CardDisplay({ data }: CardDisplayProps) {
  if (!data || data.length === 0) {
    return <div className="text-slate-400">No data to display</div>;
  }

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Summary</h3>
      <div className="grid grid-cols-1 gap-4">
        {data.map((item: any, index: number) => (
          <div
            key={index}
            className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6"
          >
            <p className="text-slate-200 text-sm font-medium mb-2">
              {item.label || Object.keys(item)[0]}
            </p>
            <p className="text-3xl font-bold text-white">
              {typeof item.value === 'number'
                ? isNaN(item.value)
                  ? '0'
                  : item.value.toLocaleString('en-US', {
                      maximumFractionDigits: 0,
                    })
                : item.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
