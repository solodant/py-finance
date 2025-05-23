## py-finance application

Приложение для финансовой аналитики

Первоначальная установка:
    python -m venv venv
    pip install -r requirements.txt

Возможности:
    - Загрузка данных об акциях с API Yahoo Finance
    - Импорт данных из файлов CSV и Excel формата
    - Визуализация цены, доходности и волотильности

Функционал CLI:
    1) python app.py --key NAME --period TIME

    --key: ключ --сsv, --excel или --ticker (для Yahoo Finance)
    NAME: в случае с csv и excel - путь до файла
          в случае с ticker - тикер акции (например, AAPL)
    --period: задание периода
    TIME: период (например, 1mo, 1y, max, ytd)

    2) tox вызывается для тестов