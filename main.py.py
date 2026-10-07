"""
Главный модуль приложения Crypto Rate Tracker.
Реализует графический интерфейс на tkinter, таблицу курсов,
ручное и автоматическое обновление, обработку ошибок.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from api_client import fetch_prices, CoinGeckoError
from config import COINS, COIN_NAMES, REFRESH_INTERVAL


class CryptoApp(tk.Tk):
    """Основное окно приложения."""

    def __init__(self):
        super().__init__()
        self.title("Crypto Rate Tracker — курсы к USD")
        self.geometry("720x460")
        self.minsize(640, 400)

        self.autorefresh_var = tk.BooleanVar(value=True)
        self._after_id = None  # id запланированного автообновления

        self._build_ui()
        self.refresh()          # первая загрузка
        self._schedule_refresh()

    # ---------- Построение интерфейса ----------
    def _build_ui(self):
        # Верхняя панель
        top = ttk.Frame(self, padding=(10, 6))
        top.pack(fill="x")

        self.time_label = ttk.Label(top, text="Обновлено: —")
        self.time_label.pack(side="left")

        refresh_btn = ttk.Button(top, text="🔄 Обновить", command=self.refresh)
        refresh_btn.pack(side="right")

        # Таблица курсов
        columns = ("name", "ticker", "price", "change")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)

        headers = {
            "name":   ("Монета",      200),
            "ticker": ("Тикер",        80),
            "price":  ("Цена (USD)",  160),
            "change": ("Изм. 24ч",    130),
        }
        for col, (title, width) in headers.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="center")

        # Цветовые теги для роста/падения
        self.tree.tag_configure("up",   foreground="#0a8a0a")
        self.tree.tag_configure("down", foreground="#c0392b")

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        # Нижняя панель
        bottom = ttk.Frame(self, padding=(10, 4))
        bottom.pack(fill="x")

        chk = ttk.Checkbutton(
            bottom,
            text=f"Автообновление ({REFRESH_INTERVAL} сек)",
            variable=self.autorefresh_var,
            command=self._toggle_autorefresh,
        )
        chk.pack(side="left")

        self.status_label = ttk.Label(bottom, text="Готово", anchor="e")
        self.status_label.pack(side="right")

    # ---------- Обновление данных ----------
    def refresh(self):
        """Запрашивает данные и перерисовывает таблицу."""
        self.status_label.config(text="Загрузка...")
        self.update_idletasks()

        try:
            data = fetch_prices(COINS)
        except CoinGeckoError as err:
            self.status_label.config(text=f"Ошибка: {err}")
            messagebox.showerror("Ошибка получения данных", str(err))
            return

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение
        for coin_id in COINS:
            info = data.get(coin_id)
            if not info:
                continue

            name, ticker = COIN_NAMES.get(coin_id, (coin_id.capitalize(), coin_id[:3].upper()))
            price = info.get("usd", 0.0)
            change = info.get("usd_24h_change") or 0.0

            arrow = "▲" if change >= 0 else "▼"
            tag = "up" if change >= 0 else "down"

            # Форматирование цены: большие суммы — без копеек, мелкие — 4 знака
            if price >= 1:
                price_str = f"${price:,.2f}"
            else:
                price_str = f"${price:,.4f}"

            self.tree.insert(
                "",
                "end",
                values=(name, ticker, price_str, f"{arrow} {change:+.2f} %"),
                tags=(tag,),
            )

        self.time_label.config(text=f"Обновлено: {datetime.now():%H:%M:%S}")
        self.status_label.config(text="OK")

    # ---------- Автообновление ----------
    def _schedule_refresh(self):
        """Планирует следующее автообновление."""
        if self.autorefresh_var.get():
            self._after_id = self.after(REFRESH_INTERVAL * 1000, self._auto_tick)

    def _auto_tick(self):
        """Срабатывает по таймеру."""
        self.refresh()
        self._schedule_refresh()

    def _toggle_autorefresh(self):
        """Включает/выключает автообновление."""
        if self.autorefresh_var.get():
            self._schedule_refresh()
            self.status_label.config(text="Автообновление включено")
        else:
            if self._after_id is not None:
                self.after_cancel(self._after_id)
                self._after_id = None
            self.status_label.config(text="Автообновление выключено")


if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()