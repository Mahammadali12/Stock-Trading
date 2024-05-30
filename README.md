# Stock-Trading Project

## Overview

The Stock-Trading project is a sophisticated web application designed to simulate stock trading. It utilizes Python and the Flask framework, providing an interactive platform for users to engage in stock market activities.

## Key Features

- **User Authentication**: Secure registration and login system.
- **Stock Quotes Retrieval**: Real-time stock prices through API integration.
- **Trading Functionality**: Buy and sell stocks within the application.
- **Portfolio Management**: Monitor and manage your stock holdings.
- **Transaction History**: Detailed record of all trading activities.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mahammadali12/Stock-Trading.git
   cd Stock-Trading
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

5. **Run the application:**
   ```bash
   flask run
   ```

## Usage

- **Register/Login**: Create a new account or log in to an existing one.
- **View Stock Prices**: Check real-time stock prices.
- **Trade Stocks**: Execute buy and sell orders.
- **Manage Portfolio**: View and manage your investments.
- **Track History**: Review your trading history and performance.

## Project Structure

- `app.py`: Main application script.
- `helpers.py`: Utility functions for the application.
- `templates/`: HTML templates for the web interface.
- `static/`: Static assets like CSS and JavaScript files.
- `finance.db`: SQLite database.
- `requirements.txt`: Python dependencies.

## License

This project is licensed under the MIT License. For more details, see the `LICENSE` file.

## Contact

For inquiries or issues, please visit the [GitHub repository](https://github.com/Mahammadali12/Stock-Trading).