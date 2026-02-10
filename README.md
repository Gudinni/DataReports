# Economic Data Reports
Скрипт на Python для обработки макроэкономических данных из CSV-файлов и формирования отчётов. Реализован один отчёт — average-gdp: среднее арифметическое ВВП по странам за все доступные годы, отсортированное по убыванию.
Скрипт использует стандартную библиотеку Python (argparse, csv) для основной логики и tabulate для вывода таблицы в консоль.

## Установка зависимостей
  ```Bash
    pip install tabulate
```

## Для запуска тестов:
   ```Bash
   pip install pytest
```

## Пример запуска
```Bash
python main.py --files economic1.csv economic2.csv --report average-gdp
```
Выводится таблица с ранжированием стран по среднему ВВП.
<img width="1122" height="645" alt="1" src="https://github.com/user-attachments/assets/b5ab313c-1d91-4ef7-820a-6ff64ba46b15" />


## Как добавить новый отчёт

1. **Напишите функцию с сигнатурой:**
      ```Python
      def new_report_name(rows: list[dict]) -> tuple[list[str], list[list[str]]]:
        # возвращает заголовки и строки данных
      ```
    
2. **Добавьте её в словарь REPORTS в main.py:**
```Python
REPORTS["new-report-name"] = new_report_name
```

3. Добавьте название в choices аргумента --report в parse_args().

После этого новый отчёт сразу доступен через --report new-report-name.

## Тесты
```Bash
pytest -v
```
