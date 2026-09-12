"use client";

import { Star, ShieldCheck, ArrowUpRight } from "lucide-react";

export default function ProductCard({ product, currency }) {
  const { title, price, currency: prodCurrency, platform, image_url, star_rating, review_count, product_url, dealScore } = product;
  const rating = star_rating || "4.8";
  const reviews = review_count || "150";

  let convertedPrice = price;
  if (prodCurrency !== currencyKey(currency.symbol)) {
     convertedPrice = (price * currency.rate).toFixed(0);
  } else {
     convertedPrice = price.toFixed(0);
  }

  function currencyKey(sym) {
    if (sym.includes("$")) return "USD";
    if (sym.includes("د.إ")) return "AED";
    if (sym.includes("€")) return "EUR";
    if (sym.includes("£")) return "GBP";
    return "USD";
  }

  const getPlatformStyle = (p) => {
    switch(p) {
      case 'Amazon': return { bg: 'bg-amber-500/10', text: 'text-amber-500', border: 'border-amber-500/30', glow: 'group-hover:shadow-[0_0_20px_rgba(245,158,11,0.2)]' };
      case 'Noon': return { bg: 'bg-yellow-400/10', text: 'text-yellow-400', border: 'border-yellow-400/30', glow: 'group-hover:shadow-[0_0_20px_rgba(250,204,21,0.2)]' };
      case 'Dubizzle': return { bg: 'bg-red-500/10', text: 'text-red-500', border: 'border-red-500/30', glow: 'group-hover:shadow-[0_0_20px_rgba(239,68,68,0.2)]' };
      case 'eBay': return { bg: 'bg-blue-500/10', text: 'text-blue-500', border: 'border-blue-500/30', glow: 'group-hover:shadow-[0_0_20px_rgba(59,130,246,0.2)]' };
      default: return { bg: 'bg-white/5', text: 'text-gray-400', border: 'border-white/10', glow: 'group-hover:shadow-lg' };
    }
  };

  const style = getPlatformStyle(platform);
  const condition = platform === 'Dubizzle' ? 'Used-Excellent' : 'New';

  return (
    <a 
      href={product_url}
      target="_blank"
      rel="noopener noreferrer"
      className={`group flex flex-col sm:flex-row items-start sm:items-center p-4 sm:p-3 h-auto sm:h-32 w-full bg-[#F7F7F7]/[0.02] backdrop-blur-xl rounded-2xl border border-[#F7F7F7]/5 hover:border-[#F7F7F7]/20 hover:bg-[#F7F7F7]/[0.04] transition-all duration-300 relative cursor-pointer ${style.glow}`}
    >
      
      {/* Product Image Thumbnail */}
      <div className="h-40 sm:h-full w-full sm:w-28 flex-shrink-0 bg-white rounded-xl flex items-center justify-center p-2 mb-4 sm:mb-0 sm:mr-5 shadow-inner">
        {image_url ? (
          <img 
            src={`https://wsrv.nl/?url=${encodeURIComponent(image_url)}&default=https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80`}
            alt={title}
            className="w-full h-full object-contain filter group-hover:scale-110 transition-transform duration-500 mix-blend-multiply"
            loading="lazy"
          />
        ) : (
           <div className="w-full h-full flex items-center justify-center"><span className="text-[10px] text-white drop-shadow-md">No Image</span></div>
        )}
      </div>

      {/* Main Content Area */}
      <div className="flex flex-col sm:flex-row flex-1 items-start sm:items-center h-auto sm:h-full w-full gap-4 sm:gap-6">
        
        {/* Title & Price Column */}
        <div className="flex flex-col flex-1 min-w-0 pr-0 sm:pr-6 border-b sm:border-b-0 sm:border-r border-[#F7F7F7]/10 w-full pb-4 sm:pb-0 h-auto sm:h-full justify-center">
          <div className="flex items-center gap-2 mb-2">
            <span className={`px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest border ${style.bg} ${style.text} ${style.border}`}>
              {platform}
            </span>
            {dealScore === 'great' && (
              <span className="px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest border bg-emerald-500/20 text-emerald-400 border-emerald-500/30 flex items-center gap-1 shadow-[0_0_10px_rgba(52,211,153,0.3)]">
                🔥 Great Deal
              </span>
            )}
            {dealScore === 'fair' && (
              <span className="px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest border bg-white/5 text-gray-300 border-white/10 flex items-center gap-1">
                ✓ Fair Price
              </span>
            )}
            {dealScore === 'poor' && (
              <span className="px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest border bg-red-500/10 text-red-400 border-red-500/20 flex items-center gap-1">
                🧊 Above Average
              </span>
            )}
          </div>
          <h3 className="text-sm font-semibold text-white font-medium line-clamp-1 leading-relaxed group-hover:text-white font-bold drop-shadow-lg transition-colors">{title}</h3>
          <div className="flex items-baseline gap-1.5 mt-1.5">
            <span className="text-sm font-bold text-white drop-shadow-md">{currencyKey(currency.symbol)}</span>
            <span className="text-2xl font-black text-white font-bold drop-shadow-lg tracking-tight drop-shadow-sm">{convertedPrice}</span>
          </div>
        </div>

        {/* Condition Column */}
        <div className="flex flex-row sm:flex-col items-center sm:items-start justify-between w-full sm:w-28 flex-shrink-0 sm:pl-2">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-200 font-bold uppercase tracking-widest mb-1 hidden sm:block">Condition</span>
            <span className="text-sm text-white font-medium font-semibold truncate">{condition}</span>
            {platform === 'eBay' && <span className="text-[10px] text-[#AAAE7F] mt-1.5 flex items-center gap-1 font-bold"><ShieldCheck size={12}/> Verified</span>}
          </div>

          {/* Rating Column - Moved inline on mobile */}
          <div className="flex flex-col items-end justify-center w-auto sm:w-24 flex-shrink-0 sm:pr-4">
            <div className="flex items-center gap-1.5 mb-0 sm:mb-1.5">
              <span className="text-lg font-bold text-white font-medium">{rating || "4.8"}</span>
              <Star size={16} className="text-[#D0D6B3] fill-[#D0D6B3] filter drop-shadow-[0_0_5px_rgba(208,214,179,0.4)]" />
            </div>
            <span className="text-[11px] text-gray-200 font-semibold hidden sm:block">({reviews || "150"} reviews)</span>
          </div>
        </div>
        
        {/* Link Arrow */}
        <div className="hidden sm:flex w-8 justify-center items-center opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 duration-300">
           <ArrowUpRight className="text-[#AAAE7F]" size={24} />
        </div>

      </div>
    </a>
  );
}
