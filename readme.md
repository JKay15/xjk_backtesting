# An Event-Driven Quantitative Trading Backtesting Engine in Python


1. Overview
This project presents a lightweight, event-driven quantitative trading backtesting engine built in Python. It is inspired by the popular backtrader framework but has been streamlined and re-architected to prioritize modularity, extensibility, and performance for rapid strategy research and validation.
2. Core Features
Event-Driven Architecture: Built on a core event-driven loop, ensuring high modularity and making it easy to extend with new components like custom data feeds, analyzers, or brokers.
PyTorch-like Strategy Interface: Design complex trading strategies with an intuitive, modular class structure inspired by PyTorch's nn.Module. This allows researchers to focus on algorithmic logic rather than boilerplate code.
Multi-Asset & Multi-Timeframe Support:
The powerful DataFeed class natively supports a wide range of asset classes, including stocks, futures, options, funds, and cryptocurrencies.
Seamlessly handles multiple time granularities from tick-level to daily, weekly, and yearly data, enabling the development and testing of sophisticated multi-timeframe strategies.
Advanced Position Sizing & Management: Decoupled Sizer and Position classes allow for sophisticated risk and capital management logic, independent of the core strategy execution.
Performance-Aware Design: Incorporates performance optimization techniques such as multithreading for data processing and vectorized operations (optional) with NumPy to accelerate backtests on standard hardware.
Rich Analytics & Visualization Suite:
Integrates seamlessly with TA-Lib for a comprehensive library of technical indicators.
Provides multiple plotting backends including matplotlib, pyfolio for professional tear sheets, and interactive HTML reports for dynamic result exploration.
Built-in Factor Analysis: The Analyzer module allows for easy tracking and comparison of custom metrics (e.g., returns, volatility, drawdown) across different strategy runs, facilitating robust quantitative factor research with minimal setup.
3. Project Structure
code
Code
.
├── backtesting/          # Core source code of the backtesting engine
├── data/                 # Sample data for various assets (stocks, futures, etc.)
├── futures_strategies/   # Example strategies for futures, including tick-based and trend-following models
├── stock_strategies/     # Example strategies for stocks, including moving average, momentum, trend, and channel-based models, as well as an example of a neural network strategy
├── multi_period_example/ # Demonstrates multi-timeframe backtesting capabilities
├── sizer_example/        # Demonstrates the position sizing and management functionalities
├── plotting_example/     # Showcases the various plotting and analytics features
└── nn_integration_example/ # Shows how to integrate a neural network model into a strategy
4. Roadmap & Future Work
Performance Enhancements: Further performance gains could be achieved by profiling and compiling critical hot-spots (e.g., datetime handling) with Cython. A more ambitious direction involves re-implementing the core event-driven engine in a high-performance language like C++ or Rust.
Expanded Strategy Library: The framework can be extended to include more modern and cutting-edge strategies from recent academic literature, beyond the classic strategies currently implemented.
Comprehensive Documentation: Developing a full-fledged documentation site (e.g., using Sphinx or MkDocs) with user guides and API references to improve usability for other researchers and developers.
