# Automated Quantitative Portfolio & Risk Engine (`quant-matrix-allocator`)

![Build Status](https://github.com/jamesruga/quant-matrix-allocator/workflows/Portfolio%20Allocator%20%26%20Risk%20Pipeline/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![MLOps](https://img.shields.io/badge/MLOps-CI%2FCD-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

An end-to-end, serverless quantitative asset allocation and risk management engine. It automatically optimizes multi-asset portfolio weights using Mean-Variance Sharpe Maximization, computes historical Value at Risk (VaR 95%), runs automated unit test suites (`pytest`), and renders updated visual allocation artifacts daily via GitHub Actions.

---

## 📐 Mathematical Formulation

### 1. Portfolio Return & Volatility
- **Expected Return:** $E[R_p] = w^T \mu$
- **Portfolio Variance:** $\sigma_p^2 = w^T \Sigma w$

### 2. Sharpe Ratio Optimization
$$\max_w \frac{w^T \mu - R_f}{\sqrt{w^T \Sigma w}} \quad \text{s.t.} \quad \sum_{i=1}^{N} w_i = 1, \quad 0 \le w_i \le 1$$

### 3. Historical Value at Risk (VaR 95%)
$$VaR_{0.95} = -\text{Percentile}_{5}(R_p)$$

---

## 📊 Live Visual Artifact

![Portfolio Allocation](portfolio_allocation.png)

> **How to Read This Artifact**
> * **Optimal Weights**: Bars reflect portfolio allocation calculated via SciPy's Mean-Variance Optimization (`scipy.optimize.minimize`) aiming to maximize the Sharpe ratio ($0.83$) under long-only constraints ($\sum w_i = 1, w_i \ge 0$).
> * **Risk Profiles**: Zero-weight allocations (Global Bonds, Crypto Index) indicate sub-optimal risk-adjusted yield relative to the covariance structure during optimization.
> * **Data Source & Pipeline**: Inputs are generated from a multivariate daily returns matrix ($N=1000$ simulation steps) calibrated against historical asset covariance matrices. $95\%$ Historical VaR ($1.25\%$) is computed directly from the 5th percentile of simulated portfolio return distributions ($VaR_{0.95} = -\text{Percentile}_5(R_p)$).

---

## 🛠️ Tech Stack & Quality Gates

* **Core Analytics**: Python 3.10, NumPy, Pandas, SciPy
* **Visualization**: Matplotlib, Seaborn
* **Testing & CI/CD**: Pytest, GitHub Actions
