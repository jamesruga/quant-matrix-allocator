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

## 📊 Live Visual Artifacts

![Portfolio Allocation](portfolio_allocation.png)

---

## 🛠 Tech Stack & Quality Gates

- **Core Analytics:** Python 3.10, NumPy, Pandas, SciPy (`scipy.optimize.minimize`)
- **Data Visualization:** Matplotlib, Seaborn
- **Testing & Quality Assurance:** Pytest (Matrix sanity, long-only bounds, weight sum constraints)
- **CI/CD Automation:** GitHub Actions (Scheduled daily execution at `22:00 UTC` / `01:00 EAT`)

---

## 🚀 Local Quickstart

```bash
git clone [https://github.com/jamesruga/quant-matrix-allocator.git](https://github.com/jamesruga/quant-matrix-allocator.git)
cd quant-matrix-allocator
pip install -r requirements.txt
pytest tests/
python src/allocator.py
```
