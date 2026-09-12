"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const PLATFORM_COLORS = {
  Amazon: "#f59e0b",   // Amber
  eBay: "#60a5fa",     // Blue
  Noon: "#facc15",     // Yellow
  Dubizzle: "#f87171", // Red
};

export default function PriceChart({ data, currency }) {
  
  const bestPrices = {};
  data.forEach((item) => {
    if (item.price > 0) {
      if (!bestPrices[item.platform] || item.price < bestPrices[item.platform].price) {
        bestPrices[item.platform] = item;
      }
    }
  });

  const chartData = Object.values(bestPrices).map((item) => ({
    name: item.platform,
    price: item.price * currency.rate,
    fullName: item.title.length > 30 ? item.title.substring(0, 30) + "..." : item.title,
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-[#143109] border border-[#F7F7F7]/10 p-4 rounded-xl shadow-2xl max-w-[220px]">
          <p className="text-gray-200 text-[10px] font-bold uppercase tracking-widest mb-1.5">{payload[0].payload.name} Best Deal</p>
          <p className="text-white font-medium text-sm font-medium leading-snug mb-2">{payload[0].payload.fullName}</p>
          <p className="text-white font-bold drop-shadow-lg text-lg font-black">{currency.symbol} {payload[0].value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-80 mt-4 flex flex-col">
      <h3 className="text-sm font-semibold mb-6 text-white drop-shadow-md tracking-wide uppercase">Lowest Price Comparison</h3>
      <div className="flex-grow min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 25 }}>
            <XAxis dataKey="name" stroke="#52525b" fontSize={11} tickLine={false} axisLine={false} dy={15} interval={0} />
            <YAxis stroke="#52525b" fontSize={11} tickLine={false} axisLine={false} width={50} tickFormatter={(value) => value.toLocaleString()} />
            <Tooltip content={<CustomTooltip />} cursor={{fill: 'rgba(255,255,255,0.03)'}} />
            <Bar dataKey="price" radius={[4, 4, 0, 0]} maxBarSize={40}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={PLATFORM_COLORS[entry.name] || "#8b5cf6"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
