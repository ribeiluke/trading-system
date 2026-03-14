'use client';

import { useState } from 'react';

const FAQS = [
  {
    q: 'Is my money safe with AlphaBot?',
    a: 'Absolutely. AlphaBot uses read-only API keys for market analysis and only requests trading permissions when you explicitly enable them. Your funds always remain in your personal exchange account — we never custody your assets. All API keys are encrypted at rest with AES-256.',
  },
  {
    q: 'Which exchanges do you support?',
    a: 'We support all major exchanges including Binance, Binance Futures, Coinbase Advanced, Kraken, Bybit, OKX, KuCoin and more. We continuously add new exchanges based on user demand.',
  },
  {
    q: 'Do I need trading experience to use AlphaBot?',
    a: 'Not at all! AlphaBot is designed for every experience level. Beginners can use our one-click pre-built strategies, while seasoned traders can craft custom logic using our advanced strategy builder and backtesting engine.',
  },
  {
    q: 'Can I cancel my subscription anytime?',
    a: 'Yes — cancel anytime with zero penalties or hidden fees. Your bots continue running until the end of your current billing period, and you keep all historical data and reports.',
  },
  {
    q: "What's the minimum investment required?",
    a: "AlphaBot charges no minimum trading capital. We recommend starting with at least $500 to run most strategies effectively. Your subscription fee is completely separate from your trading capital.",
  },
  {
    q: 'How is AlphaBot different from other trading bots?',
    a: "AlphaBot uses advanced market microstructure analysis combined with ATR-based dynamic risk management and real-time signal processing — the same methodology powering our Pullback ATR strategy. Our algorithms are backed by over $2.8B in cumulative trading volume and continuous market-adaptive optimisation.",
  },
];

export default function FAQSection() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section id="faq" className="py-24">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-6">
            <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-blue-400 text-sm font-medium">FAQ</span>
          </div>
          <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
            Frequently Asked{' '}
            <span className="gradient-text">Questions</span>
          </h2>
          <p className="text-slate-400 text-lg">Everything you need to know before getting started</p>
        </div>

        <div className="space-y-3">
          {FAQS.map((faq, i) => (
            <div
              key={i}
              className={`bg-[#0a1628] border rounded-2xl overflow-hidden transition-all duration-300 ${
                open === i ? 'border-blue-500/40' : 'border-[#1e3a5f]/60 hover:border-[#2d5a8e]/60'
              }`}
            >
              <button
                className="w-full text-left px-6 py-5 flex items-center justify-between gap-4 group"
                onClick={() => setOpen(open === i ? null : i)}
              >
                <span className="text-white font-semibold text-sm sm:text-base">{faq.q}</span>
                <div
                  className={`flex-shrink-0 w-7 h-7 rounded-full border flex items-center justify-center transition-all duration-300 ${
                    open === i
                      ? 'border-blue-500 bg-blue-500/20 rotate-45'
                      : 'border-[#2d5a8e] group-hover:border-blue-400/50'
                  }`}
                >
                  <svg className="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16M4 12h16" />
                  </svg>
                </div>
              </button>
              {open === i && (
                <div className="px-6 pb-6">
                  <p className="text-slate-400 text-sm leading-relaxed">{faq.a}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
