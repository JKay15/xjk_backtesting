# Event-Driven Quantitative Trading Backtesting Engine

## 1. Overview

This project presents a lightweight, event-driven quantitative trading backtesting engine built in Python. Inspired by the popular `backtrader` framework, it has been streamlined and re-architected to prioritize **modularity**, **extensibility**, and **performance**. It serves as a robust foundation for rapid strategy research, factor analysis, and algorithmic trading simulation.

## 2. Core Features

*   **🚀 Event-Driven Architecture**
    Built on a core event-driven loop, ensuring high modularity. This design allows for easy extension with custom components (DataFeeds, Analyzers, Brokers) without modifying the core engine.

*   **🧠 PyTorch-like Strategy Interface**
    Design complex trading strategies with an intuitive, modular class structure inspired by PyTorch's `nn.Module`. This familiar API allows researchers to focus on algorithmic logic rather than boilerplate code.

*   **📈 Multi-Asset & Multi-Timeframe Support**
    *   **Universal Asset Support:** The powerful `DataFeed` class natively supports a wide range of asset classes, including **stocks, futures, options, funds, and cryptocurrencies**.
    *   **Granular Control:** Seamlessly handles multiple time granularities from **tick-level** to **daily, weekly, and yearly** data. It supports sophisticated multi-timeframe strategies (e.g., trading on ticks based on daily trends).

*   **🛡️ Advanced Position & Risk Management**
    Decoupled `Sizer` and `Position` classes allow for sophisticated risk control and capital management logic, independent of the core strategy execution signals.

*   **⚡ Performance-Aware Design**
    Incorporates performance optimization techniques such as **multithreading** for data processing and **vectorized operations** (optional) with NumPy to accelerate backtests on standard hardware.

*   **📊 Rich Analytics & Visualization**
    *   **Indicator Library:** Integrates seamlessly with `TA-Lib` for a comprehensive library of technical indicators.
    *   **Visualization:** Provides multiple plotting backends including `matplotlib`, `pyfolio` for professional tear sheets, and interactive HTML reports for dynamic result exploration.
    *   **Factor Analysis:** The `Analyzer` module allows for easy tracking and comparison of custom metrics (e.g., Returns, Volatility, Sharpe Ratio, Max Drawdown) across different strategy runs.

## 3. Project Structure

```text
.
├── backtesting/          # Core source code of the backtesting engine
├── data/                 # Sample data for various assets (stocks, futures, etc.)
├── futures_strategies/   # Example strategies for futures (tick-based, trend-following, etc.)
├── stock_strategies/     # Example strategies for stocks (Moving Average, Momentum, Neural Networks)
├── multi_period_example/ # Demonstrates multi-timeframe backtesting capabilities
├── sizer_example/        # Demonstrates position sizing and management functionalities
├── plotting_example/     # Showcases plotting and analytics features
└── nn_integration_example/ # Demonstrates integration of Neural Network models into strategies
```

## 4. Roadmap & Future Work

- **Performance Enhancements**
  - Profile and compile critical hot-spots (e.g., datetime handling) using Cython.
  - Explore re-implementing the core event loop in a high-performance language like C++ or Rust for production-grade speed.

- **Expanded Strategy Library**
  - Implement modern, cutting-edge strategies from recent academic literature (beyond the classic technical analysis strategies).

- **Documentation**
  - Develop a full-fledged documentation site (e.g., using Sphinx or MkDocs) with user guides and API references.
