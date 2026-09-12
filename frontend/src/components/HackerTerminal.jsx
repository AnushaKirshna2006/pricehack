"use client";

import { useState, useEffect } from "react";

const LOG_MESSAGES = [
  "[+] Initializing scraper engine...",
  "[+] Bypassing WAF (Web Application Firewall)...",
  "[+] Rotating Proxy (IP: 192.168.1.104)...",
  "[+] Accessing Amazon Search...",
  "[+] Scraping ASIN metadata...",
  "[+] Accessing eBay Search...",
  "[+] Compiling cross-platform results...",
  "[+] Applying smart filter algorithms...",
  "[+] Optimizing results for maximum value...",
  "[+] Payload ready. Downloading..."
];

export default function HackerTerminal() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      if (index < LOG_MESSAGES.length) {
        setLogs((prev) => [...prev, LOG_MESSAGES[index]]);
        index++;
      } else {
        clearInterval(interval);
      }
    }, 400); // Add a new log every 400ms for that fast hacking feel

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto mt-8 glass rounded-xl overflow-hidden shadow-2xl shadow-blue-500/20 border border-blue-500/30">
      {/* Terminal Header */}
      <div className="bg-gray-900/80 px-4 py-2 flex items-center border-b border-gray-800">
        <div className="flex space-x-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
        </div>
        <div className="mx-auto text-xs text-gray-400 font-mono">system@pricehack: ~/scrapers</div>
      </div>
      
      {/* Terminal Body */}
      <div className="p-4 bg-[#050505]/90 min-h-[250px] font-mono text-sm">
        {logs.map((log, i) => (
          <div key={i} className="text-green-400 mb-1 animate-pulse">
            <span className="text-blue-400 mr-2">{new Date().toISOString().split('T')[1].slice(0, 8)}</span>
            {log}
          </div>
        ))}
        {logs.length < LOG_MESSAGES.length && (
          <div className="text-green-400 mt-2">
            <span className="animate-ping inline-block w-2 h-4 bg-green-400 align-middle"></span>
          </div>
        )}
      </div>
    </div>
  );
}
