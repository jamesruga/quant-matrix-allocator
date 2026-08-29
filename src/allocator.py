import numpy as np
import pandas as pd
from scipy.optimize import minimize

def generate_synthetic_returns(n_days=1000, seed=42):
    np.random.seed(seed)
    assets = ['US_Equities', 'Global_Bonds', 'Gold', 'Crypto_Index']
    mean_returns = np.array([0.12, 0.04, 0.06, 0.25]) / 252

    # Synthetic covariance construction
    volatilities = np.array([0.18, 0.05, 0.15, 0.60]) / np.sqrt(252)
    corr_matrix = np.array([
        [1.00, -0.15,  0.10,  0.30],
        [-0.15, 1.00,  0.25, -0.05],
        [0.10,  0.25,  1.00,  0.05],
        [0.30, -0.05,  0.05,  1.00]
    ])
    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix

    returns = np.random.multivariate_normal(mean_returns, cov_matrix, n_days)
    return pd.DataFrame(returns, columns=assets)

def optimize_portfolio(returns_df, risk_free_rate=0.02):
    mean_returns = returns_df.mean() * 252
    cov_matrix = returns_df.cov() * 252
    n_assets = len(mean_returns)

    def negative_sharpe(weights):
        p_return = np.dot(weights, mean_returns)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -(p_return - risk_free_rate) / p_vol

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = tuple((0.0, 1.0) for _ in range(n_assets))
    initial_weights = np.array([1.0 / n_assets] * n_assets)

    result = minimize(negative_sharpe, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    if not result.success:
        raise RuntimeError("Optimization failed to converge.")

    opt_weights = result.x
    opt_return = np.dot(opt_weights, mean_returns)
    opt_vol = np.sqrt(np.dot(opt_weights.T, np.dot(cov_matrix, opt_weights)))
    sharpe = (opt_return - risk_free_rate) / opt_vol

    # Historical Value at Risk (95%)
    portfolio_daily_returns = returns_df.dot(opt_weights)
    var_95 = -np.percentile(portfolio_daily_returns, 5)

    return {
        'weights': dict(zip(returns_df.columns, opt_weights)),
        'expected_return': opt_return,
        'volatility': opt_vol,
        'sharpe_ratio': sharpe,
        'var_95': var_95
    }

def render_allocation_chart(results, output_path='portfolio_allocation.png'):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))

    assets = list(results['weights'].keys())
    weights = [results['weights'][a] * 100 for a in assets]

    palette = sns.color_palette("viridis", len(assets))
    bars = plt.bar(assets, weights, color=palette, edgecolor='black', linewidth=1)

    plt.ylabel('Allocation Weight (%)', fontsize=11, fontweight='bold')
    plt.title(f"Optimal Mean-Variance Portfolio (Sharpe: {results['sharpe_ratio']:.2f} | VaR 95%: {results['var_95']*100:.2f}%)",
              fontsize=12, fontweight='bold', pad=12)
    plt.ylim(0, max(weights) * 1.2 if max(weights) > 0 else 100)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == '__main__':
    data = generate_synthetic_returns()
    metrics = optimize_portfolio(data)
    print(f"[Engine Output] Optimized Sharpe Ratio: {metrics['sharpe_ratio']:.4f}")
    print(f"[Engine Output] 95% Daily VaR: {metrics['var_95']*100:.2f}%")
    render_allocation_chart(metrics)
    print("[Engine Output] Saved visual artifact: portfolio_allocation.png")
