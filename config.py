"""
Конфигурация приложения Crypto Rate Tracker.
Содержит список отслеживаемых монет, интервал автообновления
и человекочитаемые названия криптовалют.
"""

# Список идентификаторов монет для CoinGecko API
COINS = [
    "bitcoin",
    "ethereum",
    "binancecoin",
    "solana",
    "ripple",
    "cardano",
    "dogecoin",
]

# Человекочитаемые названия и тикеры
COIN_NAMES = {
    "bitcoin":     ("Bitcoin",      "BTC"),
    "ethereum":    ("Ethereum",     "ETH"),
    "binancecoin": ("Binance Coin", "BNB"),
    "solana":      ("Solana",       "SOL"),
    "ripple":      ("XRP",          "XRP"),
    "cardano":     ("Cardano",      "ADA"),
    "dogecoin":    ("Dogecoin",     "DOGE"),
}

# Интервал автообновления (в секундах)
REFRESH_INTERVAL = 60

# Базовый URL CoinGecko API
API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Таймаут HTTP-запроса (в секундах)
REQUEST_TIMEOUT = 10