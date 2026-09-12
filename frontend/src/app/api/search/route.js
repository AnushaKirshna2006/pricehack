import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const body = await request.json();
    // Use API_URL from environment, fallback to localhost for local development
    const backendUrl = process.env.API_URL || 'http://127.0.0.1:8000';
    
    // Explicitly proxy the request to the Python backend
    const res = await fetch(`${backendUrl}/api/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    
    if (!res.ok) {
      throw new Error(`Python backend failed with status: ${res.status}`);
    }
    
    const data = await res.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error("API Proxy Error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
