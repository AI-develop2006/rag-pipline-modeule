import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { message } = body;

    if (!message) {
      return NextResponse.json(
        { error: "Message content is required." },
        { status: 400 }
      );
    }

    // Fallback to localhost:8000 if BACKEND_API_URL is not set
    const backendUrl = process.env.BACKEND_API_URL || "http://localhost:8000";

    const backendResponse = await fetch(`${backendUrl}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!backendResponse.ok) {
      const errorDetails = await backendResponse.text();
      return NextResponse.json(
        { error: `Backend service responded with an error: ${errorDetails}` },
        { status: backendResponse.status }
      );
    }

    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Internal server error proxying chat request." },
      { status: 500 }
    );
  }
}
