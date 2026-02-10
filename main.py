import argparse
import csv
from collections import defaultdict
from typing import Callable
from tabulate import tabulate


def parse_args():
    parser = argparse.ArgumentParser(description="data reports")
    parser.add_argument(
        '--files', 
        nargs='+', 
        required=True, 
        help="Paths to CSV files with data",
    )
    parser.add_argument(
        '--report', 
        required=True, 
        choices=['average-gdp'], 
        help="Report currently only average-gdp",
    )
    return parser.parse_args()


def read_data(file_paths: list[str]):
    rows: list[dict[str, float | str]] = []

    numeric_keys = {'gdp', 'gdp_growth', 'inflation', 'unemployment', 'population'}

    for path in file_paths:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                processed_row = {}
                for key, value in row.items():
                    if key in numeric_keys and value.strip():
                        try:
                            processed_row[key] = float(value)
                        except ValueError:
                            processed_row[key] = value
                    else:
                        processed_row[key] = value
                rows.append(processed_row)
    return rows


def generate_average_gdp(rows: list[dict[str, float | str]]):

    country_gdps: defaultdict[str, list[float]] = defaultdict(list)

    for row in rows:
        country = row['country']
        gdp = row.get('gdp')
        if isinstance(gdp, float):
            country_gdps[country].append(gdp)

    averages = {
        country: sum(gdps) / len(gdps)
        for country, gdps in country_gdps.items()
        if gdps
    }

    sorted_items = sorted(averages.items(), key=lambda x: x[1], reverse=True)

    report_rows = [[country, f'{avg:.2f}'] for country, avg in sorted_items]

    headers = ['country', 'gdp']
    return headers, report_rows

REPORTS: dict[str, Callable[[list[dict]], tuple[list[str], list[list[str]]]]] = {
    'average-gdp': generate_average_gdp,
}


def main():
    args = parse_args()

    if args.report not in REPORTS:
        raise ValueError(f"Unknown report: {args.report}")
    
    data_rows = read_data(args.files)
    headers, report_rows = REPORTS[args.report](data_rows)

    table_rows = []
    for rank, row in enumerate(report_rows, start=1):
        table_rows.append([rank] + row)

    full_headers = [""] + headers

    print(
        tabulate(
            table_rows,
            headers=full_headers,
            tablefmt='psql',
            colalign=('right', 'left', 'right'),
        )
    )
            

if __name__ == '__main__':
    main()