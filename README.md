# 📊 py-finance

**py-finance** — это приложение для финансовой аналитики, позволяющее загружать, визуализировать и анализировать данные из различных источников.

---

## 🚀 Установка

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

---

## ⚙️ Возможности

- 📈 Загрузка данных об акциях через API [Yahoo Finance](https://finance.yahoo.com/)
- 📂 Импорт данных из файлов форматов **CSV** и **Excel**
- 📊 Визуализация **цены**, **доходности** и **волатильности**

---

## 🖥️ Использование CLI

```bash
python app.py --key <KEY> --period <TIME>
```

### Аргументы:

- `--key`:
  - `--csv` — путь к CSV-файлу
  - `--excel` — путь к Excel-файлу
  - `--ticker` — тикер акции (например, `AAPL`)
- `--period <TIME>` — период анализа:
  - Примеры: `1mo`, `6mo`, `1y`, `ytd`, `max`

---

## ✅ Запуск тестов

```bash
tox
```

---

## 📎 Пример использования

```bash
python app.py --key --ticker AAPL --period 6mo
```

---
