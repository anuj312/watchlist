import pandas as pd
from datetime import datetime, timedelta
from kiteconnect import KiteConnect
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# ================= CONFIG =================
API_KEY = "ikfiyrgi5w2dttxb"
ACCESS_TOKEN = "1eksEcZi4gtSkgk4CWXHFDvYc7hq9Iwg"

LOOKBACK_DAYS = 20
BUFFER_DAYS = 60   # enough to skip weekends + holidays
TOP_N = 10



# ================= CONSOLE =================
console = Console()

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
        "SBILIFE", "LICHSGFIN", "LICI", "MANAPPURAM", 'IRFC', "IIFL", "CDSL"
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
    ]
}
SYMBOLS = sorted(set(sum(SECTOR_DEFINITIONS.values(), [])))

# ================= KITE INIT =================
console.print("\n[bold cyan]🔌 Connecting to Kite...[/bold cyan]")
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# ================= LOAD INSTRUMENTS =================
inst = pd.DataFrame(kite.instruments("NSE"))
inst = inst[inst.tradingsymbol.isin(SYMBOLS)]
symbol_token = dict(zip(inst.tradingsymbol, inst.instrument_token))

console.print(f"[green]✔ Loaded {len(symbol_token)} symbols[/green]")

# ================= DATE RANGE =================
today = datetime.now().date()
from_date = today - timedelta(days=BUFFER_DAYS)

results = []

# ================= DATA FETCH WITH PROGRESS =================
console.print("\n[bold yellow]📊 Fetching volume data (today vs 20D avg)...[/bold yellow]\n")

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("{task.completed}/{task.total}"),
    TimeElapsedColumn(),
    console=console,
) as progress:

    task = progress.add_task("Processing stocks", total=len(symbol_token))

    for sym, token in symbol_token.items():
        try:
            df = pd.DataFrame(
                kite.historical_data(token, from_date, today, "day")
            )

            if len(df) < LOOKBACK_DAYS + 1:
                progress.advance(task)
                continue

            today_vol = df.iloc[-1]["volume"]
            avg_20d = df.iloc[-LOOKBACK_DAYS-1:-1]["volume"].mean()
            ratio = today_vol / avg_20d if avg_20d else 0

            results.append({
                "symbol": sym,
                "today_volume": int(today_vol),
                "avg_20d_volume": int(avg_20d),
                "volume_ratio": round(ratio, 2)
            })

        except Exception as e:
            console.print(f"[red]❌ {sym} failed[/red]")

        progress.advance(task)

# ================= RESULT DF =================
df = pd.DataFrame(results)

if df.empty:
    console.print("[bold red]⚠️ No data fetched. Exiting.[/bold red]")
    exit()

# ================= TOP VOLUME TABLE =================
top_table = Table(title="🔝 Top Volume Expansion Stocks (Today vs 20D Avg)", header_style="bold green")
top_table.add_column("Symbol", style="cyan")
top_table.add_column("Today Vol", justify="right")
top_table.add_column("20D Avg Vol", justify="right")
top_table.add_column("Vol Ratio", justify="right", style="bold green")

for _, r in df.sort_values("volume_ratio", ascending=False).head(TOP_N).iterrows():
    top_table.add_row(
        r["symbol"],
        f"{r['today_volume']:,}",
        f"{r['avg_20d_volume']:,}",
        f"{r['volume_ratio']}"
    )

# ================= LOW VOLUME TABLE =================
low_table = Table(title="🔻 Lowest Volume Stocks (Drying Participation)", header_style="bold red")
low_table.add_column("Symbol", style="cyan")
low_table.add_column("Today Vol", justify="right")
low_table.add_column("20D Avg Vol", justify="right")
low_table.add_column("Vol Ratio", justify="right", style="bold red")

for _, r in df.sort_values("volume_ratio", ascending=True).head(TOP_N).iterrows():
    low_table.add_row(
        r["symbol"],
        f"{r['today_volume']:,}",
        f"{r['avg_20d_volume']:,}",
        f"{r['volume_ratio']}"
    )

# ================= DISPLAY =================
console.print()
console.print(top_table)
console.print()
console.print(low_table)
console.print("\n[bold green]✅ Scan Complete[/bold green]\n")
