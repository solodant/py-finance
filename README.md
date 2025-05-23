# 📊 py-finance

**py-finance** — приложение для финансовой аналитики.

---

## 🚀 Установка

```bash
python -m venv venv
```
```bash
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```
```bash
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

- `Вместо --key`:
  - `--csv <путь к CSV-файлу>`
  - `--excel <путь к Excel-файлу>`
  - `--ticker <тикер акции>` (прим. тикера `AAPL`)
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
python app.py --ticker AAPL --period 6mo
```

---
