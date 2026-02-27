// ─── PRICE TRENDS ─────────────────────────────────────────────────────────────
// Shape: { [itemName]: [{ date, buy, sell }] }
// Future: fetch from GET /api/price-trends?item=Ash+Prime+Set

export const PRICE_TRENDS = {
  "Ash Prime Set": [
    { date: "Feb 1",  buy: 120, sell: 145 },
    { date: "Feb 3",  buy: 118, sell: 142 },
    { date: "Feb 5",  buy: 125, sell: 150 },
    { date: "Feb 7",  buy: 130, sell: 158 },
    { date: "Feb 9",  buy: 128, sell: 155 },
    { date: "Feb 11", buy: 135, sell: 162 },
    { date: "Feb 13", buy: 140, sell: 168 },
    { date: "Feb 15", buy: 138, sell: 165 },
    { date: "Feb 17", buy: 145, sell: 172 },
    { date: "Feb 19", buy: 150, sell: 178 },
    { date: "Feb 21", buy: 148, sell: 175 },
    { date: "Feb 23", buy: 155, sell: 183 },
  ],
  "Nidus Prime Set": [
    { date: "Feb 1",  buy: 200, sell: 235 },
    { date: "Feb 3",  buy: 195, sell: 230 },
    { date: "Feb 5",  buy: 210, sell: 245 },
    { date: "Feb 7",  buy: 205, sell: 240 },
    { date: "Feb 9",  buy: 215, sell: 252 },
    { date: "Feb 11", buy: 220, sell: 258 },
    { date: "Feb 13", buy: 218, sell: 255 },
    { date: "Feb 15", buy: 225, sell: 263 },
    { date: "Feb 17", buy: 230, sell: 268 },
    { date: "Feb 19", buy: 228, sell: 265 },
    { date: "Feb 21", buy: 235, sell: 274 },
    { date: "Feb 23", buy: 240, sell: 280 },
  ],
  "Primed Continuity": [
    { date: "Feb 1",  buy: 80,  sell: 95  },
    { date: "Feb 3",  buy: 82,  sell: 97  },
    { date: "Feb 5",  buy: 79,  sell: 93  },
    { date: "Feb 7",  buy: 85,  sell: 100 },
    { date: "Feb 9",  buy: 88,  sell: 103 },
    { date: "Feb 11", buy: 86,  sell: 101 },
    { date: "Feb 13", buy: 90,  sell: 106 },
    { date: "Feb 15", buy: 92,  sell: 108 },
    { date: "Feb 17", buy: 89,  sell: 105 },
    { date: "Feb 19", buy: 94,  sell: 110 },
    { date: "Feb 21", buy: 96,  sell: 113 },
    { date: "Feb 23", buy: 98,  sell: 115 },
  ],
};

// ─── TOP TRADED ITEMS ─────────────────────────────────────────────────────────
// Shape: [{ name, volume, change }]
// Future: fetch from GET /api/top-items

export const TOP_ITEMS = [
  { name: "Nidus Prime Set",      volume: 842, change: 12.4  },
  { name: "Ash Prime Set",        volume: 731, change: 8.1   },
  { name: "Primed Continuity",    volume: 614, change: -3.2  },
  { name: "Blind Rage",           volume: 589, change: 5.7   },
  { name: "Octavia Prime Set",    volume: 503, change: -1.8  },
  { name: "Arcane Energize",      volume: 477, change: 22.3  },
  { name: "Adaptation",           volume: 445, change: 9.0   },
  { name: "Zaw Strike: Dehtat",   volume: 398, change: -6.5  },
];

// ─── SPREAD DATA ──────────────────────────────────────────────────────────────
// Shape: [{ item, buy, sell, spread }]
// Future: fetch from GET /api/spreads

export const SPREAD_DATA = [
  { item: "Arcane Energize",   buy: 185, sell: 220, spread: 35 },
  { item: "Nidus Prime Set",   buy: 240, sell: 280, spread: 40 },
  { item: "Ash Prime Set",     buy: 155, sell: 183, spread: 28 },
  { item: "Blind Rage",        buy: 42,  sell: 55,  spread: 13 },
  { item: "Primed Continuity", buy: 98,  sell: 115, spread: 17 },
  { item: "Adaptation",        buy: 30,  sell: 40,  spread: 10 },
];

// ─── STATS SUMMARY ────────────────────────────────────────────────────────────
// Shape: [{ label, value, delta, up }]
// Future: fetch from GET /api/summary

export const STATS_SUMMARY = [
  { label: "Active Listings", value: "24,891", delta: "+3.2%",  up: true  },
  { label: "Avg Sell Price",  value: "182 ₱",  delta: "+5.8%",  up: true  },
  { label: "Avg Spread",      value: "23.8 ₱", delta: "-1.1%",  up: false },
  { label: "Orders Today",    value: "6,447",  delta: "+14.3%", up: true  },
];