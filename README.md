# Quantum Computing in Finance 👨‍💻
## Hi 👋  This is a proof of concept repository for Qiskit Finance application, here we go! 🚀

***
### General Info
> In this repository we will navigate and develop a portfolio optimization proof of concept using Qiskit. For this experiment we will use as data input, the prices of the main cryptocurrencies.
The objective is to be able to find the best combination of cryptocurrencies for an investment portfolio, based on its historical performance.

> Disclaimer: The focus of this repository is to bring readers closer to the different functions that Qiskit Financial Application has, it is in no way about investment advice.

## Comparison status

Choosing from Binance data and filtering for USDT ending assets, taken only the 25 first.

| Solver      | Solution | Time  |
|-------------|----------|-------|
| Brute force | Optimal  | 14.6s |
| CVX         | Optimal  |  29ms |

Updated: January 8, 2022

## Building and installing the library

Creating a virtual environment is more than recommended:

```
python -m venv <venv_name>
```

Afterwards, one can just build the library:

```
python -m build
```

And proceed to install it using the route of the library *dist/quanvia-x.x.x....whl* by a simple pip install routine. Enjoy!

WIP
