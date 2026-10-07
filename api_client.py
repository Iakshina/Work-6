"""
Модуль для взаимодействия с публичным API CoinGecko.
Отвечает за получение текущих курсов криптовалют к USD.
"""

import requests
from config import API_URL, REQUEST_TIMEOUT


class CoinGeckoError(Exception):
    """Собственное исключение для ошибок API."""
    pass


def fetch_prices(coins: list[str]) -> dict:
    """
    Запрашивает у CoinGecko цены и изменение за 24 часа.

    :param coins: список идентификаторов монет (например, ["bitcoin", "ethereum"])
    :return: словарь вида
             {"bitcoin": {"usd": 67432.10, "usd_24h_change": 2.31}, ...}
    :raises CoinGeckoError: при ошибке сети или некорректном ответе
    """
    if not coins:
        raise CoinGeckoError("Список монет пуст.")

    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.Timeout as exc:
        raise CoinGeckoError("Превышено время ожидания ответа от CoinGecko.") from exc
    except requests.ConnectionError as exc:
        raise CoinGeckoError("Нет соединения с интернетом или CoinGecko недоступен.") from exc
    except requests.HTTPError as exc:
        raise CoinGeckoError(f"HTTP-ошибка: {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise CoinGeckoError(f"Ошибка запроса: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise CoinGeckoError("Некорректный JSON в ответе API.") from exc

    if not isinstance(data, dict) or not data:
        raise CoinGeckoError("API вернул пустой ответ или неизвестный формат.")

    return data