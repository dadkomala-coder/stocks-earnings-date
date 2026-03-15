import yfinance as yf
from datetime import datetime, date

## Script describes earning dates for your favorite stocks. If the earnings date is less than 31 days from the current date, highlight it in blue.

BLUE = "\033[94m"
RESET = "\033[0m"

tickers = ["META", "TSLA", "PBR", "OXY", "WTI", "AVGO", "TTD", "NVDA", "SAP"]
today = date.today()

for symbol in tickers:
    try:
        cal = yf.Ticker(symbol).calendar
        raw = None

        if isinstance(cal, dict):
            raw = cal.get("Earnings Date")
        elif isinstance(cal, list) and cal:
            raw = cal[0]

        if raw is None:
            print(f"{symbol:6} → no data is available")
            continue

        # Normalize to a date string
        if isinstance(raw, list):
            raw = raw[0]
        d = raw if isinstance(raw, str) else str(raw)
        nice = d[:10]

        # Highlight if within 31 days
        earnings_dt = datetime.strptime(nice, "%Y-%m-%d").date()
        days_away = (earnings_dt - today).days
        color = BLUE if 0 <= days_away <= 31 else RESET

        print(f"{color}{symbol:6} → Next earnings: {nice}{RESET}")

    except Exception as e:
        print(f"{symbol:6} → error: {e}")

print("\n If dates are missing check https://finance.yahoo.com/calendar/earnings")