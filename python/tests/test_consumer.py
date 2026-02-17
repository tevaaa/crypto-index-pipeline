import pytest
from consumer import calculate_index
from config import INDEX_WEIGHTS

#     "BTC": 0.25,
#     "ETH": 0.30,
#     "SOL": 0.20,
#     "XRP": 0.15,
#     "BNB": 0.10,


def test_index_starts_at_1000():
    base = {s: 100.0 for s in INDEX_WEIGHTS}
    latest = {s: 100.0 for s in INDEX_WEIGHTS}
    assert calculate_index(base, latest, INDEX_WEIGHTS) == 1000.0

def test_index_reflects_price_change():
    base = {s: 100.0 for s in INDEX_WEIGHTS}
    latest = {s: 100.0 for s in INDEX_WEIGHTS}
    latest["BTC"] = 110.0  # +10%
    # 0.25 WEIGHT, 10% * 0.25 = 2.5% increase
    assert calculate_index(base, latest, INDEX_WEIGHTS) == pytest.approx(1025.0)

def test_index_all_double():
    base = {s: 100.0 for s in INDEX_WEIGHTS}
    latest = {s: 200.0 for s in INDEX_WEIGHTS}
    assert calculate_index(base, latest, INDEX_WEIGHTS) == pytest.approx(2000.0)

def test_index_partial_prices():
    base = {"BTC": 100.0}
    latest = {"BTC": 100.0}
    result = calculate_index(base, latest, INDEX_WEIGHTS)
    assert result < 1000
