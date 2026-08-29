import pytest
import numpy as np
import pandas as pd
from src.allocator import generate_synthetic_returns, optimize_portfolio

@pytest.fixture
def sample_data():
    return generate_synthetic_returns(n_days=500, seed=123)

def test_data_shape(sample_data):
    assert sample_data.shape == (500, 4)
    assert not sample_data.isnull().values.any()

def test_optimization_weights_sum(sample_data):
    res = optimize_portfolio(sample_data)
    total_weight = sum(res['weights'].values())
    assert np.isclose(total_weight, 1.0, atol=1e-4)

def test_long_only_bounds(sample_data):
    res = optimize_portfolio(sample_data)
    for weight in res['weights'].values():
        assert weight >= -1e-6  # allow tiny floating point tolerance

def test_var_positive(sample_data):
    res = optimize_portfolio(sample_data)
    assert res['var_95'] > 0
