'use client';

import { useState } from 'react';

const plans = [
  {
    name: 'Starter',
    monthly: 29,
    annual: 23,
    description: 'Perfect for beginners exploring automated crypto trading',
    popular: false,
    features: [
      '1 Active Trading Bot',
      '3 Pre-built Strategies',
      'Basic Portfolio Analytics',
      'Email Alerts',
      'Binance & Coinbase Support',
      '5 Backtests / Month',
      'Community Support',
    ],
    cta: 'Get Started Free',
    ctaClass: 'border border-[#1e3a5f] hover:border-blue-500/50 text-white hover:bg-[#0f1f3d]',
    cardClass: 'bg-[#0a1628] border border-[#1e3a5f]/60',
  },
  {
    name: 'Pro',
    monthly: 79,
    annual: 63,
    description: 'Ideal for serious traders maximising consistent returns',
    popular: true,
    features: [
      '5 Active Trading Bots',
      'All 12+ Strategies',
      'Advanced Portfolio Analytics',
      'Telegram + Email Alerts',
      '8 Exchange Integrations',
      'Unlimited Backtests',
      'Priority Support',
      'Full API Access',
      'DCA & Grid Bots',
    ],
    cta: 'Start Free Trial',
    ctaClass: 'bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white shadow-lg shadow-blue-500/30',
    cardClass: 'bg-gradient-to-b from-[#0f2854] to-[#0a1e40] border border-blue-500/50 shadow-2xl shadow-blue-500/10',
  },
  {
    name: 'Elite',
    monthly: 199,
    annual: 159,
    description: 'For professional traders and institutional desks',
    popular: false,
    features: [
      'Unlimited Trading Bots',
      'Custom Strategy Builder',
      'Institutional-grade Analytics',
      'Multi-channel Smart Alerts',
      'All Exchanges + DEX Support',
      'Unlimited Backtests',
      'Dedicated Account Manager',
      'White-label Option',
      'Custom API Integrations',
      'SLA Uptime Guarantee',
    ],
    cta: 'Contact Sales',
    ctaClass: 'border border-[#1e3a5f] hover:border-blue-500/50 text-white hover:bg-[#0f1f3d]',
    cardClass: 'bg-[#0a1628] border border-[#1e3a5f]/60',
  },
];

export default function PricingSection() {
  const [annual, setAnnual] = useState(false);

  return (
    <section id="pricing" className="py-24 relative">
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[900px] bg-blue-500/5 rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        {/* Section header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-6">
            <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-blue-400 text-sm font-medium">Simple Pricing</span>
          </div>
          <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
            Choose Your{' '}
            <span className="gradient-text">Trading Edge</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-10">
            7-day free trial on all plans. No credit card required. Cancel anytime.
          </p>

          {/* Toggle */}
          <div className="inline-flex items-center bg-[#0a1628] border border-[#1e3a5f]/60 rounded-full p-1.5">
            <button
              onClick={() => setAnnual(false)}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                !annual ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' : 'text-slate-400 hover:text-white'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setAnnual(true)}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition-all duration-200 flex items-center gap-2 ${
                annual ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' : 'text-slate-400 hover:text-white'
              }`}
            >
              Annual
              <span className="bg-emerald-500 text-white text-xs px-2 py-0.5 rounded-full font-bold">
                Save 20%
              </span>
            </button>
          </div>
        </div>

        {/* Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 items-center">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl p-8 transition-all duration-300 ${plan.cardClass} ${
                plan.popular ? 'md:scale-105 md:z-10' : 'card-glow'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 whitespace-nowrap">
                  <span className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white text-xs font-bold px-5 py-1.5 rounded-full shadow-lg shadow-blue-500/30">
                    ✦ MOST POPULAR
                  </span>
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-1">{plan.name}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{plan.description}</p>
              </div>

              <div className="mb-7">
                <div className="flex items-end gap-1">
                  <span className="text-slate-400 text-lg mb-1">$</span>
                  <span className="text-5xl font-extrabold text-white tabular-nums">
                    {annual ? plan.annual : plan.monthly}
                  </span>
                  <span className="text-slate-400 text-sm mb-2">/mo</span>
                </div>
                {annual && (
                  <p className="text-emerald-400 text-xs mt-1 font-medium">
                    Billed ${(plan.annual * 12).toLocaleString()}/year · Save ${((plan.monthly - plan.annual) * 12)}
                  </p>
                )}
              </div>

              <a
                href="#"
                className={`block w-full text-center py-3 px-6 rounded-full font-semibold text-sm transition-all duration-200 hover:scale-105 mb-8 ${plan.ctaClass}`}
              >
                {plan.cta}
              </a>

              <ul className="space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3 text-sm text-slate-300">
                    <svg className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Guarantee */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-4 bg-[#0a1628] border border-[#1e3a5f]/60 rounded-2xl px-8 py-4">
            <svg className="w-8 h-8 text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <div className="text-left">
              <p className="text-white font-semibold text-sm">30-Day Money-Back Guarantee</p>
              <p className="text-slate-400 text-xs mt-0.5">Not satisfied? Get a full refund, no questions asked.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
