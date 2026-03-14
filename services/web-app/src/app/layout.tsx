import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "AlphaBot — AI-Powered Crypto Trading Bots",
    template: "%s | AlphaBot",
  },
  description:
    "Automate your crypto trading with cutting-edge AI bots. 24/7 automated trading, real-time signals, and proven strategies. Start your free 7-day trial today.",
  keywords: [
    "crypto trading bot",
    "automated trading",
    "bitcoin bot",
    "algorithmic trading",
    "trading signals",
    "ATR strategy",
    "pullback trading",
  ],
  openGraph: {
    title: "AlphaBot — AI-Powered Crypto Trading Bots",
    description:
      "Automate your crypto trading with cutting-edge AI bots. 24/7 automated trading, real-time signals, and proven strategies.",
    siteName: "AlphaBot",
    locale: "en_US",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
