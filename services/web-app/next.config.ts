import type { NextConfig } from "next";


const nextConfig: NextConfig = {
  // Enable React strict mode for best practices
  reactStrictMode: true,
  // Proxy API requests in development to FastAPI backend
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : "http://api-gateway:8000/api/:path*",
      },
    ];
  },
};

export default nextConfig;
