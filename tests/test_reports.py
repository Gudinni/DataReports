import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import read_data, generate_average_gdp


@pytest.fixture
def sample_csv_files(tmp_path: Path):
    file1 = tmp_path / 'econ1.csv'
    file1.write_text(
        """country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,27000,2.0,3.0,3.7,330,North America
United States,2022,25000,1.5,8.0,3.6,329,North America
China,2023,18000,5.0,2.0,5.0,1400,Asia
"""
    )

    file2 = tmp_path / 'econ2.csv'
    file2.write_text(
        """country,year,gdp,gdp_growth,inflation,unemployment,population,continent
China,2021,17000,8.0,1.0,5.5,1400,Asia
Germany,2023,4000,0.0,6.0,3.0,83,Europe
"""
    )

    return [str(file1), str(file2)]

def test_read_data(sample_csv_files):
    rows = read_data(sample_csv_files)
    assert len(rows) == 5
    assert rows[0]['country'] == 'United States'
    assert isinstance(rows[0]['gdp'], float)


def test_generate_average_gdp(sample_csv_files):
    rows = read_data(sample_csv_files)
    headers, report_rows = generate_average_gdp(rows)

    assert headers == ['country', 'gdp']

    expected = [
        ["United States", "26000.00"],
        ["China", "17500.00"],
        ["Germany", "4000.00"],
    ]

    assert report_rows == expected