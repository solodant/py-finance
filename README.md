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

- 📈 Загрузка данных об акциях и валютах через API [Yahoo Finance](https://finance.yahoo.com/)
- 📂 Импорт данных из файлов форматов **CSV** и **Excel**
- 📊 Визуализация **цены**, **доходности** и **волатильности** акций
- 📊 Визуализация **стоимости** и **корреляции** курсов валют

---

## 🖥️ Использование CLI

```bash
python app.py --key KEY --period TIME
```

### Аргументы:

- `Вместо --key KEY`:
  - `--csv путь/к/файлу.csv`
  - `--excel путь/к/файлу.xlsx или файлу.xls`
  - `--ticker тикер акции`
  - `--currencies пара валют`
- `Опционально --period TIME`

---

## 📎 Пример использования

```bash
python app.py --ticker AAPL --period 6mo
```
```bash
python app.py --currencies USDRUB EURRUB JPYRUB GBPRUB --period ytd
```

---

## ✅ Запуск тестов

```bash
tox
```

---
