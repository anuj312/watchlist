from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# ================= SECTORS =================
SECTOR_DEFINITIONS = {
    "METAL": [
        "ADANIENT", "HINDALCO", "JSWSTEEL", "HINDZINC", "APLAPOLLO",
        "TATASTEEL", "JINDALSTEL", "VEDL", "SAIL", "NATIONALUM", "NMDC"
    ],
    "PSUS": [
        "BANKINDIA", "PNB", "INDIANB", "SBIN", "UNIONBANK",
        "BANKBARODA", "CANBK"
    ],
    "REALTY": [
        "PHOENIXLTD", "GODREJPROP", "LODHA", "OBEROIRLTY",
        "DLF", "PRESTIGE", "NBCC", "NCC"
    ],
    "ENERGY": [
        "CGPOWER", "RELIANCE", "GMRAIRPORT", "JSWENERGY", "ONGC",
        "POWERGRID", "BLUESTARCO", "COALINDIA", "SUZLON", "IREDA",
        "IOC", "IGL", "TATAPOWER", "INOXWIND", "MAZDOCK", "PETRONET",
        "SOLARINDS", "ADANIGREEN", "NTPC", "OIL", "BDL", "BPCL",
        "NHPC", "POWERINDIA", "ADANIENSOL", "HINDPETRO", "TORRENTPOWER"
    ],
    "AUTO": [
        "BOSCHLTD", "TIINDIA", "HEROMOTOCO", "M&M", "EICHERMOT",
        "EXIDEIND", "BAJAJ-AUTO", "ASHOKLEY", "MARUTI", "TITAGARH",
        "TVSMOTOR", "MOTHERSON", "SONACOMS", "UNOMINDA",
        "TMPV", "BHARATFORG"
    ],
    "IT": [
        "KAYNES", "TATATECH", "LTIM", "CYIENT", "MPHASIS",
        "TCS", "CAMS", "OFSS", "HFCL", "TECHM",
        "TATAELXSI", "HCLTECH", "WIPRO", "KPITTECH",
        "COFORGE", "PERSISTENT", "INFY"
    ],
    "PHARMA": [
        "CIPLA", "ALKEM", "BIOCON", "DRREDDY", "MANKIND",
        "TORNTPHARM", "ZYDUSLIFE", "DIVISLAB", "LUPIN",
        "PPLPHARMA", "LAURUSLABS", "FORTIS", "AUROPHARMA",
        "GLENMARK", "SUNPHARMA"
    ],
    "FMCG": [
        "ETERNAL", "MARICO", "NYKAA", "NESTLEIND", "VBL",
        "COLPAL", "HINDUNILVR", "PATANJALI", "DMART",
        "DABUR", "GODREJCP", "BRITANNIA", "UNITDSPR",
        "ITC", "TATACONSUM", "KALYANKJIL", "SUPREMEIND"
    ],
    "CEMENT": [
        "SHREECEM", "DALBHARAT", "AMBUJACEM", "ULTRACEMCO"
    ],
    "FINANCE": [
        "PNBHOUSING", "BAJAJFINSV", "ICICIPRULI", "NUVAMA", "HDFCLIFE", "SAMMAANCAP",
        "ANGELONE", "RECLTD", "BAJFINANCE", "BSE", "MAXHEALTH",
        "ICICIGI", "HUDCO", "CHOLAFIN", "PFC", "HDFCAMC", "MUTHOOTFIN",
        "PAYTM", "JIOFIN", "SHRIRAMFIN", "SBICARD", "POLICYBZR",
        "SBILIFE", "LICHSGFIN", "LICI", "MANAPPURAM", "IRFC", "IIFL", "CDSL"
    ],
    "BANK": [
        "IDFCFIRSTB", "FEDERALBNK", "INDUSINDBK",
        "HDFCBANK", "SBIN", "KOTAKBANK", "AUBANK",
        "CANBK", "BANDHANBNK", "RBLBANK",
        "ICICIBANK", "AXISBANK"
    ],
    "NIFTY_50": [
        "ADANIENT","ADANIPORTS","APOLLOHOSP","ASIANPAINT","AXISBANK",
        "BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BEL","BHARTIARTL",
        "CIPLA","COALINDIA","DRREDDY","EICHERMOT","GRASIM",
        "HCLTECH","HDFCBANK","HDFCLIFE","HINDALCO","HINDUNILVR",
        "ICICIBANK","INFY","INDIGO","ITC","JIOFIN","JSWSTEEL",
        "KOTAKBANK","LT","M&M","MARUTI","MAXHEALTH","NESTLEIND",
        "NTPC","ONGC","POWERGRID","RELIANCE","SBILIFE","SHRIRAMFIN",
        "SBIN","SUNPHARMA","TCS","TATACONSUM","TATASTEEL",
        "TECHM","TITAN","TRENT","ULTRACEMCO","WIPRO",
        "TATAMOTORS","ETERNAL"
    ],
    "MIDCAP": [
        "RVNL", "MPHASIS", "HINDPETRO", "PAGEIND", "POLYCAB",
        "LUPIN", "IDFCFIRSTB", "CONCOR", "CUMMINSIND", "VOLTAS",
        "BHARATFORG", "FEDERALBNK", "INDHOTEL", "COFORGE",
        "ASHOKLEY", "PERSISTENT", "UPL", "GODREJPROP",
        "AUROPHARMA", "AUBANK", "ASTRAL", "HDFCAMC",
        "JUBLFOOD", "PIIND"
    ],
    "INDICES": [
        "CNXENERGY","CNXCONSUMPTION","CNXREALTY","NIFTY_OIL_AND_GAS",
        "CNXPHARMA","CNXIT","NIFTY_HEALTHCARE","CNXFMCG",
        "CNXFINANCE","NIFTY_CONSR_DURBL","CNXAUTO","CNXMETAL"
    ]
}

# ================= FASTAPI =================
app = FastAPI(title="TradingView Watchlist")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def index():
    sidebar = ""
    for sector, stocks in SECTOR_DEFINITIONS.items():
        sidebar += f"""
        <div class="sector collapsed" onclick="toggleSector(this)">{sector}</div>
        <div class="sector-group">
        """
        for s in stocks:
            sidebar += f"""
            <div class="stock" data-symbol="{s}">
              <div class="stock-left">
                <span class="stock-name" onclick="selectStock(this.closest('.stock'))">{s}</span>
                <span class="open-new" onclick="openStockNewTab(event,'{s}')">↗</span>
              </div>
              <span class="star" onclick="toggleFav(event,'{s}')">☆</span>
            </div>
            """
        sidebar += "</div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Watchlist</title>
<script src="https://s3.tradingview.com/tv.js"></script>

<style>
/* ===== GLOBAL ===== */
body {{
  margin:0;
  height:100vh;
  display:flex;
  background:radial-gradient(1200px 600px at 10% 10%, #0f172a, #020617);
  font-family:Inter,system-ui,-apple-system;
  color:#e5e7eb;
}}

#chart {{ flex:1; position:relative; }}
#tv {{ height:100%; }}

/* ===== OPEN TV BUTTON ===== */
#open-tv {{
  position:absolute;
  top:14px;
  right:18px;
  z-index:10;
  background:linear-gradient(135deg,#111827,#020617);
  color:#e5e7eb;
  border:1px solid rgba(37,99,235,.6);
  padding:7px 12px;
  font-size:12px;
  font-weight:700;
  border-radius:8px;
  cursor:pointer;
  box-shadow:0 6px 20px rgba(0,0,0,.4);
}}
#open-tv:hover {{
  background:#2563eb;
}}

/* ===== SIDEBAR ===== */
#sidebar {{
  width:340px;
  background:linear-gradient(180deg,#020617,#020617 60%,#01040a);
  overflow-y:auto;
  border-left:1px solid rgba(148,163,184,.15);
}}

#resizer {{
  width:6px;
  cursor:col-resize;
  background:linear-gradient(180deg,#020617,#020617);
}}

/* ===== HEADER ===== */
.header {{
  padding:18px 16px;
  font-size:22px;
  backdrop-filter: blur(8px);
  font-weight:900;
  letter-spacing:1px;
  text-transform:uppercase;

  color:#f8fafc;

  background:
    linear-gradient(
      135deg,
      #1e40af,
      #2563eb 40%,
      #22d3ee
    );

  border-bottom:1px solid rgba(255,255,255,0.15);

  position:sticky;
  top:0;
  z-index:20;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.45),
    inset 0 -1px 0 rgba(255,255,255,0.2);
}}

.header::after {{
  content:"";
  position:absolute;
  left:16px;
  bottom:6px;
  width:48px;
  height:3px;
  border-radius:999px;
  background:linear-gradient(90deg,#fde68a,#facc15);
}}

.header:hover {{
  box-shadow:
    0 12px 40px rgba(37,99,235,0.45),
    inset 0 -1px 0 rgba(255,255,255,0.25);
}}


/* ===== FAVORITES ===== */
.fav-header {{
  margin:12px 12px 6px;
  padding:10px 14px;
  font-size:12px;
  font-weight:900;
  letter-spacing:1.2px;
  text-transform:uppercase;
  color:#fde68a;
  background:linear-gradient(90deg,rgba(250,204,21,.25),rgba(251,191,36,.15));
  border:1px solid rgba(250,204,21,.4);
  border-radius:10px;
  cursor:pointer;
  position:relative;
}}

.fav-header::after {{
  content:"▾";
  position:absolute;
  right:14px;
  top:50%;
  transform:translateY(-50%);
  transition:transform .25s ease;
}}

.fav-header.collapsed::after {{
  transform:translateY(-50%) rotate(-90deg);
}}

#fav-list {{
  margin:0 12px 10px;
  overflow:hidden;
  max-height:800px;
  opacity:1;
  transition:max-height .35s cubic-bezier(.4,0,.2,1),opacity .25s ease;
}}

.fav-header.collapsed + #fav-list {{
  max-height:0;
  opacity:0;
  pointer-events:none;
}}

.fav-stock {{
  padding:8px 12px;
  font-size:13px;
  font-weight:600;
  display:flex;
  justify-content:space-between;
  align-items:center;
  border-radius:8px;
  color:#f8fafc;
  transition:all .15s ease;
}}

.fav-stock:hover {{
  background:rgba(250,204,21,.12);
}}

.fav-remove {{
  color:#f87171;
  font-weight:900;
  cursor:pointer;
}}
.fav-remove:hover {{
  color:#ef4444;
  transform:scale(1.15);
}}

/* ===== SECTORS ===== */
.sector {{
  padding:10px 14px;
  margin:8px 12px 6px;
  font-size:12px;
  font-weight:900;
  letter-spacing:1.2px;
  text-transform:uppercase;
  color:#e0f2fe;
  background:linear-gradient(90deg,rgba(37,99,235,.25),rgba(34,211,238,.15));
  border:1px solid rgba(56,189,248,.45);
  border-radius:999px;
  cursor:pointer;
  position:relative;
}}

.sector::after {{
  content:"▾";
  position:absolute;
  right:14px;
  top:50%;
  transform:translateY(-50%);
  transition:transform .25s ease;
}}

.sector.collapsed::after {{
  transform:translateY(-50%) rotate(-90deg);
}}

.sector-group {{
  margin:0 8px 6px;
  overflow:hidden;
  max-height:2000px;
  opacity:1;
  transition:max-height .35s cubic-bezier(.4,0,.2,1),opacity .25s ease;
}}

.sector.collapsed + .sector-group {{
  max-height:0;
  opacity:0;
  pointer-events:none;
}}

/* ===== STOCK ROW ===== */
.stock {{
  padding:7px 14px;
  margin:2px 6px;
  border-radius:8px;
  font-size:12px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  transition:all .15s ease;
}}

.stock:hover {{
  background:#1e293b;
}}

.stock.active {{
  background:linear-gradient(90deg,#2563eb,#1d4ed8);
}}

/* ===== STOCK LEFT ===== */
.stock-left {{
  display:flex;
  align-items:center;
  gap:6px;
}}

.stock-name {{
  font-size:13px;
  font-weight:600;
  letter-spacing:.2px;
  cursor:pointer;
}}

/* ===== ICONS ===== */
.star {{
  cursor:pointer;
  color:#64748b;
  font-size:18px;
}}
.star.active {{
  color:#facc15;
}}

.open-new {{
  cursor:pointer;
  color:#38bdf8;
  font-size:20px;
  font-weight:900;
  line-height:1;
}}
.open-new:hover {{
  color:#7dd3fc;
}}
</style>

</head>

<body>

<div id="chart">
  <button id="open-tv" onclick="openFullTV()">Open Full TradingView ↗</button>
  <div id="tv"></div>
</div>

<div id="resizer"></div>

<div id="sidebar">
  <div class="header">WATCHLIST</div>

  <div class="fav-header" onclick="toggleFavBox(this)">★ FAVORITES</div>
  <div id="fav-list"></div>

  {sidebar}
</div>

<script>
let widget;
let stocks=[...document.querySelectorAll('.stock')];
let favs=JSON.parse(localStorage.getItem("favs")||"[]");
let currentSymbol=null;

function loadChart(sym){{
  if(widget) widget.remove();
  widget=new TradingView.widget({{
    autosize:true,
    symbol:sym,
    interval:"1D",
    theme:"dark",
    container_id:"tv"
  }});
}}

function selectStock(el){{
  stocks.forEach(s=>s.classList.remove('active'));
  el.classList.add('active');
  currentSymbol=el.dataset.symbol;
  loadChart(currentSymbol);
}}

function openFullTV(){{
  if(!currentSymbol) return;
  window.open(
  "https://www.tradingview.com/chart/?symbol=" + currentSymbol + "&interval=1D",
  "_blank"
);

}}

function openStockNewTab(e,sym){{
  e.stopPropagation();
  window.open(
  "https://www.tradingview.com/chart/?symbol=" + currentSymbol + "&interval=1D",
  "_blank"
);

}}

function toggleSector(el){{ el.classList.toggle("collapsed"); }}
function toggleFavBox(el){{ el.classList.toggle("collapsed"); }}

function toggleFav(e,sym){{
  e.stopPropagation();
  favs=favs.includes(sym)?favs.filter(x=>x!==sym):[...favs,sym];
  localStorage.setItem("favs",JSON.stringify(favs));
  renderFavs();
}}

function renderFavs(){{
  const box=document.getElementById("fav-list");
  box.innerHTML="";
  favs.forEach(sym=>{{
    const d=document.createElement("div");
    d.className="fav-stock";

    const n=document.createElement("span");
    n.innerText=sym;
    n.onclick=()=>{{ currentSymbol=sym; loadChart(sym); }};

    const r=document.createElement("span");
    r.innerText="✕";
    r.className="fav-remove";
    r.onclick=e=>{{ e.stopPropagation(); favs=favs.filter(x=>x!==sym); localStorage.setItem("favs",JSON.stringify(favs)); renderFavs(); }};

    d.appendChild(n); d.appendChild(r); box.appendChild(d);
  }});

  document.querySelectorAll(".star").forEach(star=>{{
    star.classList.toggle("active",favs.includes(star.parentElement.parentElement.dataset.symbol));
  }});
}}

renderFavs();
if(stocks.length>0) selectStock(stocks[0]);

let resizing=false;
resizer.onmousedown=()=>resizing=true;
document.onmouseup=()=>resizing=false;
document.onmousemove=e=>{{ if(resizing) sidebar.style.width=(window.innerWidth-e.clientX)+"px"; }};
</script>

</body>
</html>
"""

