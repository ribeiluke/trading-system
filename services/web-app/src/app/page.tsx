import Navbar from './components/Navbar';
import PricingSection from './components/PricingSection';
import FAQSection from './components/FAQSection';

// ─── Static data ──────────────────────────────────────────────────────────────
const FEATURES = [
  {
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
    title: 'AI-Powered Analysis',
    desc: 'Deep learning models scan thousands of signals per second to identify high-probability setups before they happen.',
    accent: 'from-blue-500/20 to-blue-500/5',
    border: 'hover:border-blue-500/40',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: '24/7 Automated Trading',
    desc: 'Your bots never sleep. Execute trades around the clock across any time zone — even while you are offline.',
    accent: 'from-cyan-500/20 to-cyan-500/5',
    border: 'hover:border-cyan-500/40',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      </svg>
    ),
    title: 'Dynamic Risk Management',
    desc: 'ATR-based stop losses and position sizing adapt in real-time to protect your capital during volatile markets.',
    accent: 'from-emerald-500/20 to-emerald-500/5',
    border: 'hover:border-emerald-500/40',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    title: 'Real-time Signals',
    desc: 'Receive instant Telegram and email alerts the moment your bot enters or exits a position, with full transparency.',
    accent: 'from-yellow-500/20 to-yellow-500/5',
    border: 'hover:border-yellow-500/40',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
      </svg>
    ),
    title: 'Multi-Exchange Support',
    desc: 'Connect to Binance, Bybit, OKX, Kraken, Coinbase and 8+ more exchanges from a single unified dashboard.',
    accent: 'from-purple-500/20 to-purple-500/5',
    border: 'hover:border-purple-500/40',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
    title: 'Backtesting Engine',
    desc: 'Validate any strategy against years of historical data with detailed P&L reports, drawdown analysis, and Sharpe ratios.',
    accent: 'from-rose-500/20 to-rose-500/5',
    border: 'hover:border-rose-500/40',
  },
];

const STEPS = [
  {
    num: '01',
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
      </svg>
    ),
    title: 'Connect Your Exchange',
    desc: 'Link your exchange with a read-only or trading API key in under 2 minutes. Your funds never leave your account.',
  },
  {
    num: '02',
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
      </svg>
    ),
    title: 'Choose Your Strategy',
    desc: 'Pick from our battle-tested library — Pullback ATR, Trend Following, Scalping, or build a custom strategy from scratch.',
  },
  {
    num: '03',
    icon: (
      <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
          d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
      </svg>
    ),
    title: 'Watch Your Bot Trade',
    desc: 'Sit back as the AI executes trades, manages risk, and sends you real-time alerts. Monitor everything on your dashboard.',
  },
];

const STRATEGIES = [
  {
    tag: 'FEATURED',
    name: 'Pullback ATR',
    desc: 'Identifies high-momentum pullbacks using Average True Range for dynamic risk management and precision entries.',
    stats: [{ label: 'Win Rate', value: '68%' }, { label: 'Avg. R:R', value: '2.4x' }, { label: 'Drawdown', value: '<12%' }],
    color: 'border-blue-500/40 bg-gradient-to-br from-blue-500/10 to-transparent',
    badge: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  },
  {
    tag: 'POPULAR',
    name: 'Trend Following',
    desc: 'Rides confirmed macro trends with EMA crossovers and volume confirmation for sustained profit capture.',
    stats: [{ label: 'Win Rate', value: '61%' }, { label: 'Avg. R:R', value: '3.1x' }, { label: 'Drawdown', value: '<15%' }],
    color: 'border-emerald-500/40 bg-gradient-to-br from-emerald-500/10 to-transparent',
    badge: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  },
  {
    tag: 'FAST',
    name: 'Scalping Bot',
    desc: 'High-frequency strategy designed for liquid markets, capturing small but consistent gains on 1-5m timeframes.',
    stats: [{ label: 'Win Rate', value: '72%' }, { label: 'Avg. R:R', value: '1.5x' }, { label: 'Drawdown', value: '<8%' }],
    color: 'border-cyan-500/40 bg-gradient-to-br from-cyan-500/10 to-transparent',
    badge: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
  },
  {
    tag: 'SWING',
    name: 'Swing Trader',
    desc: 'Multi-day hold strategy that targets major support/resistance flips with higher reward-to-risk ratios.',
    stats: [{ label: 'Win Rate', value: '58%' }, { label: 'Avg. R:R', value: '4.2x' }, { label: 'Drawdown', value: '<18%' }],
    color: 'border-purple-500/40 bg-gradient-to-br from-purple-500/10 to-transparent',
    badge: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  },
];

const TESTIMONIALS = [
  {
    name: 'Jordan M.',
    role: 'Full-time Crypto Trader',
    avatar: 'JM',
    quote:
      'My portfolio is up 127% in 6 months since switching to AlphaBot. The Pullback ATR strategy is genuinely groundbreaking. I tried 4 other bots before this — nothing comes close.',
    stars: 5,
    gain: '+127%',
  },
  {
    name: 'Sarah K.',
    role: 'Software Engineer & Investor',
    avatar: 'SK',
    quote:
      "I set it up on a Sunday evening and by Monday morning the bot had already executed 8 profitable trades. The Telegram alerts are incredibly detailed. I'm obsessed.",
    stars: 5,
    gain: '+84%',
  },
  {
    name: 'Mike R.',
    role: 'Hedge Fund Analyst',
    avatar: 'MR',
    quote:
      "The backtesting engine is institutional quality. I validated our firm's strategy in minutes instead of weeks. The API access on the Elite plan is exactly what we needed.",
    stars: 5,
    gain: '+203%',
  },
];

const TICKER_ITEMS = [
  { sym: 'BTC/USDT', price: '$71,243', change: '+2.4%', up: true },
  { sym: 'ETH/USDT', price: '$3,891', change: '+1.8%', up: true },
  { sym: 'BNB/USDT', price: '$612', change: '+3.2%', up: true },
  { sym: 'SOL/USDT', price: '$187', change: '-0.9%', up: false },
  { sym: 'ADA/USDT', price: '$0.621', change: '+4.1%', up: true },
  { sym: 'AVAX/USDT', price: '$43.2', change: '+2.7%', up: true },
  { sym: 'DOT/USDT', price: '$9.14', change: '-1.2%', up: false },
  { sym: 'MATIC/USDT', price: '$1.02', change: '+5.3%', up: true },
];

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function Home() {
  return (
    <main className="min-h-screen bg-[#050d1a] text-white overflow-x-hidden">
      <Navbar />

      {/* ══════════════════════════════════════════════════════════════════════
          HERO
      ══════════════════════════════════════════════════════════════════════ */}
      <section className="hero-bg relative min-h-screen flex items-center pt-16">
        {/* Subtle grid overlay */}
        <div
          className="absolute inset-0 opacity-[0.04] pointer-events-none"
          style={{
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M 60 0 L 0 0 0 60' fill='none' stroke='%23ffffff' stroke-width='0.7'/%3E%3C/svg%3E\")",
          }}
        />

        {/* Orb decorations */}
        <div className="absolute top-1/4 right-0 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative w-full py-20 lg:py-28">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            {/* ── Left: Copy ── */}
            <div className="animate-fade-up">
              {/* Badge */}
              <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/25 rounded-full px-4 py-1.5 mb-8">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500" />
                </span>
                <span className="text-blue-300 text-sm font-medium">Powered by Advanced AI · Live Trading</span>
              </div>

              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold leading-[1.05] tracking-tight mb-6">
                Trade Smarter.
                <br />
                <span className="gradient-text">Profit Bigger.</span>
              </h1>

              <p className="text-slate-400 text-lg sm:text-xl leading-relaxed max-w-lg mb-10">
                Deploy AI-powered trading bots that execute 24/7, manage risk dynamically, and consistently outperform the market — all without you lifting a finger.
              </p>

              {/* CTA buttons */}
              <div className="flex flex-col sm:flex-row gap-4 mb-12">
                <a
                  href="#pricing"
                  className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold px-8 py-4 rounded-full text-base transition-all duration-200 shadow-2xl shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-105"
                >
                  Start Free 7-Day Trial
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </a>
                <a
                  href="#features"
                  className="inline-flex items-center justify-center gap-2 border border-[#1e3a5f] hover:border-blue-500/40 text-slate-300 hover:text-white font-semibold px-8 py-4 rounded-full text-base transition-all duration-200 hover:bg-[#0a1628]"
                >
                  <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  See How It Works
                </a>
              </div>

              {/* Trust signals */}
              <div className="flex flex-wrap items-center gap-6">
                {[
                  { icon: '🔒', text: 'Bank-level Security' },
                  { icon: '⚡', text: 'No Credit Card Required' },
                  { icon: '✅', text: 'Cancel Anytime' },
                ].map((t) => (
                  <div key={t.text} className="flex items-center gap-2 text-slate-400 text-sm">
                    <span>{t.icon}</span>
                    <span>{t.text}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* ── Right: Visual dashboard mockup ── */}
            <div className="relative flex justify-center lg:justify-end">
              {/* Main portfolio card */}
              <div className="animate-float relative bg-gradient-to-b from-[#0d1e38] to-[#0a1628] border border-[#1e3a5f]/80 rounded-3xl p-6 w-full max-w-sm shadow-2xl shadow-black/50">
                {/* Card header */}
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">Portfolio Value</p>
                    <p className="text-3xl font-extrabold text-white mt-1">$48,291.40</p>
                  </div>
                  <div className="flex items-center gap-1.5 bg-emerald-500/15 border border-emerald-500/25 rounded-full px-3 py-1.5">
                    <svg className="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                    </svg>
                    <span className="text-emerald-400 text-sm font-bold">+31.4%</span>
                  </div>
                </div>

                {/* Chart */}
                <div className="mb-6 rounded-2xl overflow-hidden bg-[#050d1a]/60 p-3">
                  <svg viewBox="0 0 280 90" fill="none" className="w-full">
                    <defs>
                      <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.35" />
                        <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
                      </linearGradient>
                    </defs>
                    <path
                      d="M0,75 C15,70 20,72 35,58 C50,44 58,50 72,38 C86,26 92,30 108,20 C124,10 130,14 148,9 C163,5 170,8 185,4 C200,0 210,3 225,2 C240,1 255,3 280,1 L280,90 L0,90 Z"
                      fill="url(#areaGrad)"
                    />
                    <path
                      className="animate-chart-draw"
                      d="M0,75 C15,70 20,72 35,58 C50,44 58,50 72,38 C86,26 92,30 108,20 C124,10 130,14 148,9 C163,5 170,8 185,4 C200,0 210,3 225,2 C240,1 255,3 280,1"
                      stroke="#3b82f6"
                      strokeWidth="2.5"
                      fill="none"
                      strokeLinecap="round"
                    />
                    <circle cx="280" cy="1" r="4" fill="#3b82f6" />
                    <circle cx="280" cy="1" r="8" fill="#3b82f6" fillOpacity="0.3" className="animate-ping-slow" />
                  </svg>
                </div>

                {/* Bot stats row */}
                <div className="grid grid-cols-3 gap-3 mb-4">
                  {[
                    { label: 'Total Trades', value: '1,847' },
                    { label: 'Win Rate', value: '68.3%' },
                    { label: 'Active Bots', value: '5' },
                  ].map((s) => (
                    <div key={s.label} className="bg-[#050d1a]/80 rounded-xl p-3 text-center">
                      <p className="text-white font-bold text-sm">{s.value}</p>
                      <p className="text-slate-500 text-xs mt-0.5">{s.label}</p>
                    </div>
                  ))}
                </div>

                {/* Status bar */}
                <div className="flex items-center justify-between bg-[#050d1a]/80 rounded-xl px-4 py-2.5">
                  <div className="flex items-center gap-2">
                    <span className="relative flex h-2 w-2">
                      <span className="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                    </span>
                    <span className="text-emerald-400 text-xs font-medium">Bots Running</span>
                  </div>
                  <span className="text-slate-500 text-xs">Last trade: 2m ago</span>
                </div>
              </div>

              {/* Floating notification 1 */}
              <div className="animate-float-sm absolute -top-4 -left-6 lg:-left-10 bg-[#0a1628] border border-[#1e3a5f]/80 rounded-2xl px-4 py-3 shadow-xl shadow-black/40 hidden sm:block">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-white text-xs font-semibold">BTC Long Opened</p>
                    <p className="text-emerald-400 text-xs">+$342 profit target</p>
                  </div>
                </div>
              </div>

              {/* Floating notification 2 */}
              <div className="animate-float absolute -bottom-4 -right-4 lg:-right-8 bg-[#0a1628] border border-[#1e3a5f]/80 rounded-2xl px-4 py-3 shadow-xl shadow-black/40 hidden sm:block">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-white text-xs font-semibold">Signal Detected</p>
                    <p className="text-blue-400 text-xs">ETH Pullback ATR ↗</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          LIVE TICKER
      ══════════════════════════════════════════════════════════════════════ */}
      <div className="border-y border-[#1e3a5f]/40 bg-[#080f1e] py-3">
        <div className="ticker-wrapper">
          <div className="ticker-track animate-ticker">
            {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, i) => (
              <span key={i} className="inline-flex items-center gap-3 px-8">
                <span className="text-slate-400 text-sm font-medium">{item.sym}</span>
                <span className="text-white text-sm font-bold">{item.price}</span>
                <span className={`text-sm font-semibold ${item.up ? 'text-emerald-400' : 'text-red-400'}`}>
                  {item.change}
                </span>
                <span className="text-[#1e3a5f]">•</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════════════════════════
          STATS
      ══════════════════════════════════════════════════════════════════════ */}
      <section className="py-20 border-b border-[#1e3a5f]/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { value: '$2.8B+', label: 'Trading Volume', icon: '📈' },
              { value: '12,500+', label: 'Active Traders', icon: '👥' },
              { value: '68.3%', label: 'Avg. Win Rate', icon: '🎯' },
              { value: '99.97%', label: 'Bot Uptime', icon: '⚡' },
            ].map((stat) => (
              <div key={stat.label} className="text-center group">
                <div className="text-3xl mb-2">{stat.icon}</div>
                <div className="text-4xl sm:text-5xl font-extrabold gradient-text mb-2">{stat.value}</div>
                <div className="text-slate-400 text-sm font-medium uppercase tracking-wider">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          FEATURES
      ══════════════════════════════════════════════════════════════════════ */}
      <section id="features" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-6">
              <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span className="text-blue-400 text-sm font-medium">Platform Features</span>
            </div>
            <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
              Everything You Need to{' '}
              <span className="gradient-text">Win the Market</span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Professional-grade tools once reserved for hedge funds, now accessible to everyone.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className={`feature-card ${f.border} rounded-2xl p-7 relative overflow-hidden group`}>
                <div className={`absolute inset-0 bg-gradient-to-br ${f.accent} opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />
                <div className="relative">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-5">
                    {f.icon}
                  </div>
                  <h3 className="text-white font-bold text-lg mb-2">{f.title}</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          HOW IT WORKS
      ══════════════════════════════════════════════════════════════════════ */}
      <section id="how-it-works" className="py-24 bg-gradient-to-b from-transparent via-[#080f1e] to-transparent">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-6">
              <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span className="text-blue-400 text-sm font-medium">Quick Setup</span>
            </div>
            <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
              Up &amp; Running in{' '}
              <span className="gradient-text">Under 5 Minutes</span>
            </h2>
            <p className="text-slate-400 text-lg max-w-xl mx-auto">No technical knowledge required. Just connect, configure, and profit.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            {/* Connector lines (desktop) */}
            <div className="hidden md:block absolute top-16 left-[calc(33.33%_-_16px)] right-[calc(33.33%_-_16px)] h-px bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />

            {STEPS.map((step, i) => (
              <div key={step.num} className="relative flex flex-col items-center text-center" style={{ animationDelay: `${i * 150}ms` }}>
                <div className="relative mb-6">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600/30 to-cyan-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shadow-lg shadow-blue-500/10">
                    {step.icon}
                  </div>
                  <div className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center">
                    <span className="text-white text-xs font-extrabold leading-none">{i + 1}</span>
                  </div>
                </div>
                <h3 className="text-white font-bold text-lg mb-2">{step.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          STRATEGIES
      ══════════════════════════════════════════════════════════════════════ */}
      <section id="strategies" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-6">
              <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span className="text-blue-400 text-sm font-medium">Trading Strategies</span>
            </div>
            <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
              Battle-tested{' '}
              <span className="gradient-text">Strategies</span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Each strategy is backtested across years of historical data and continuously optimised for live markets.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {STRATEGIES.map((s) => (
              <div key={s.name} className={`rounded-2xl border p-6 transition-all duration-300 card-glow ${s.color}`}>
                <div className="flex items-center justify-between mb-4">
                  <span className={`text-xs font-bold px-3 py-1 rounded-full border ${s.badge}`}>{s.tag}</span>
                </div>
                <h3 className="text-white font-bold text-lg mb-2">{s.name}</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-5">{s.desc}</p>
                <div className="space-y-2 border-t border-[#1e3a5f]/40 pt-4">
                  {s.stats.map((st) => (
                    <div key={st.label} className="flex items-center justify-between">
                      <span className="text-slate-500 text-xs">{st.label}</span>
                      <span className="text-white text-sm font-bold">{st.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          PRICING
      ══════════════════════════════════════════════════════════════════════ */}
      <PricingSection />

      {/* ══════════════════════════════════════════════════════════════════════
          TESTIMONIALS
      ══════════════════════════════════════════════════════════════════════ */}
      <section className="py-24 bg-gradient-to-b from-transparent via-[#080f1e] to-transparent">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-6">
              <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              <span className="text-blue-400 text-sm font-medium">Real Results</span>
            </div>
            <h2 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
              Traders Are{' '}
              <span className="gradient-text">Winning Big</span>
            </h2>
            <p className="text-slate-400 text-lg">Join thousands of traders who automated their way to consistent profits.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {TESTIMONIALS.map((t) => (
              <div key={t.name} className="feature-card rounded-2xl p-7 relative group">
                {/* Quote mark */}
                <div className="absolute top-5 right-6 text-blue-500/10 text-7xl font-serif leading-none select-none">&ldquo;</div>
                <div className="relative">
                  {/* Stars */}
                  <div className="flex gap-1 mb-4">
                    {Array.from({ length: t.stars }).map((_, i) => (
                      <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 24 24">
                        <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                    ))}
                  </div>
                  <p className="text-slate-300 text-sm leading-relaxed mb-6 italic">
                    &ldquo;{t.quote}&rdquo;
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center text-white text-sm font-bold">
                        {t.avatar}
                      </div>
                      <div>
                        <p className="text-white font-semibold text-sm">{t.name}</p>
                        <p className="text-slate-500 text-xs">{t.role}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-emerald-400 font-extrabold text-xl">{t.gain}</div>
                      <div className="text-slate-500 text-xs">portfolio gain</div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          FAQ
      ══════════════════════════════════════════════════════════════════════ */}
      <FAQSection />

      {/* ══════════════════════════════════════════════════════════════════════
          FINAL CTA
      ══════════════════════════════════════════════════════════════════════ */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-cyan-500/8 to-blue-600/10" />
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-blue-500/8 rounded-full blur-3xl" />
        </div>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-1.5 mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500" />
            </span>
            <span className="text-blue-300 text-sm font-medium">Limited Spots Available</span>
          </div>
          <h2 className="text-5xl sm:text-6xl font-extrabold text-white leading-tight mb-6">
            Ready to Let AI
            <br />
            <span className="gradient-text">Trade for You?</span>
          </h2>
          <p className="text-slate-400 text-xl leading-relaxed mb-10 max-w-2xl mx-auto">
            Join 12,500+ traders already using AlphaBot to grow their portfolios on autopilot. Start your free 7-day trial — no credit card needed.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <a
              href="#pricing"
              className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold px-10 py-4 rounded-full text-lg transition-all duration-200 shadow-2xl shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-105"
            >
              Start Free 7-Day Trial
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </a>
            <a
              href="#pricing"
              className="inline-flex items-center justify-center border border-[#1e3a5f] hover:border-blue-500/40 text-slate-300 hover:text-white font-semibold px-10 py-4 rounded-full text-lg transition-all duration-200 hover:bg-[#0a1628]"
            >
              View Pricing Plans
            </a>
          </div>
          <p className="text-slate-500 text-sm">
            🔒 Your funds stay on your exchange &nbsp;·&nbsp; ✅ Cancel anytime &nbsp;·&nbsp; ⚡ Setup in &lt; 5 minutes
          </p>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════════
          FOOTER
      ══════════════════════════════════════════════════════════════════════ */}
      <footer className="border-t border-[#1e3a5f]/40 bg-[#030810]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-10 mb-12">
            {/* Brand */}
            <div className="lg:col-span-2">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/30">
                  <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
                    <polyline points="16 7 22 7 22 13" />
                  </svg>
                </div>
                <span className="font-extrabold text-xl text-white">Alpha<span className="text-blue-400">Bot</span></span>
              </div>
              <p className="text-slate-400 text-sm leading-relaxed max-w-xs">
                AI-powered trading bots for the modern crypto investor. Automate your strategy, manage risk, and grow your portfolio.
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 className="text-white font-semibold text-sm mb-4 uppercase tracking-wider">Product</h4>
              <ul className="space-y-3">
                {['Features', 'Strategies', 'Pricing', 'Backtesting', 'API Docs'].map((l) => (
                  <li key={l}>
                    <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">{l}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 className="text-white font-semibold text-sm mb-4 uppercase tracking-wider">Company</h4>
              <ul className="space-y-3">
                {['About Us', 'Blog', 'Careers', 'Press', 'Contact'].map((l) => (
                  <li key={l}>
                    <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">{l}</a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Legal */}
            <div>
              <h4 className="text-white font-semibold text-sm mb-4 uppercase tracking-wider">Legal</h4>
              <ul className="space-y-3">
                {['Privacy Policy', 'Terms of Service', 'Cookie Policy', 'Risk Disclosure'].map((l) => (
                  <li key={l}>
                    <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">{l}</a>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-[#1e3a5f]/40 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-slate-500 text-sm">
              © 2026 AlphaBot. All rights reserved.
            </p>
            <p className="text-slate-600 text-xs text-center sm:text-right max-w-md">
              ⚠️ Risk Disclosure: Trading cryptocurrencies involves significant risk. Past performance is not indicative of future results.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
