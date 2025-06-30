# Options Intelligence Platform (In-Progress)

A high-performance options analytics backend designed for quantitative analysis. This platform provides a RESTful API to fetch live option chain data from Polygon.io, price contracts using sophisticated C++ models, and analyze historical volatility. Currently working on expanding capabilities by implementing new features, including machine learning driven profitability heatmaps and interactive frontend.

---

## Key Features

- **Live Option Chain Data**  
  Fetch real-time option contract data for any underlying stock, with filtering by contract type, expiration date, and strike price range.

- **High-Performance Pricing Engine**  
  Core pricing models are written in modern C++17 for maximum performance and precision.

- **Binomial Tree Model**  
  Prices both American (early-exercise) and European options. Highly optimized with loop-invariant code hoisting to minimize branching in the hot path.

- **Black-Scholes Model**  
  A fast, analytical model for pricing European options, serving as a baseline for validation.

- **Python-C++ Integration**  
  The C++ pricing engine is seamlessly exposed to Python using `pybind11`, combining C++ performance with Python's ease of use.

- **Asynchronous REST API**  
  Built with FastAPI, fully asynchronous using `httpx` for non-blocking I/O to handle high-concurrency workloads efficiently.

- **On-the-Fly Volatility Estimation**  
  A dedicated service calculates annualized historical volatility from recent market data, providing a key input for pricing models.

---

## Tech Stack

| Layer           | Technology  | Purpose                                               |
|-----------------|-------------|-------------------------------------------------------|
| Backend API     | Python (FastAPI) | Asynchronous request handling, data validation, orchestration |
| Pricing Engine  | C++17       | Performance-critical financial model calculations     |
| Integration    | pybind11    | Efficient, low-overhead Python bindings for C++ engine |
| Data Provider   | Polygon.io  | Live market data for stock prices and option contracts |
| Data Analysis   | NumPy       | Numerical operations for volatility calculation       |
| HTTP Client    | httpx       | High-performance asynchronous HTTP requests           |

---

## System Architecture

- **API Layer (FastAPI)**  
  Handles user interaction and request validation using Pydantic schemas.

- **Service Layer (Python)**  
  Calls dedicated async services for fetching data and calculations.

- **Volatility Service**  
  Fetches historical price data and calculates volatility metrics.

- **Options Service**  
  Retrieves option chain data from Polygon.io.

- **Pricing Engine (C++)**  
  Prices each contract by calling the C++ module via `pybind11` with market data inputs.

- **Response**  
  The priced data is structured and returned as JSON.

---

## API Endpoints

| Endpoint             | Method | Description                                                                                  |
|----------------------|--------|----------------------------------------------------------------------------------------------|
| `/options/`          | GET    | Retrieves a list of option contracts based on filter criteria                               |
| `/options/price`     | POST   | Calculates theoretical price of a single option using Black-Scholes or Binomial Tree models |
| `/options/chain/price` | POST   | Fetches volatility and stock data, then prices an entire option chain individually          |

---

## Setup and Usage

### Prerequisites

- Python 3.10+
- C++ compiler (MSVC for Windows, GCC/Clang for macOS/Linux)
- Git

### Steps

1. **Clone the Repository**
git clone https://github.com/vedaantmohta/options-intelligence-platform.git
cd options-intelligence-platform/backend

2. **Set Up a Virtual Environment**
python -m venv venv
activate venv

3. **Install Dependencies**
pip install -r requirements.txt

4. **Configure API Key**
Create a .env file in the backend directory and add your Polygon.io API key:
POLYGON_API_KEY="your_polygon_api_key_here"

5. **Compile the C++ Module**
Run the setup script to build the C++ pricing engine as a Python module:
python setup.py build_ext --inplace

6. **Run the Server**
Start the FastAPI server with hot-reloading:
uvicorn app.main:app --reload
Access the API
The API will be running at http://127.0.0.1:8000.
Use the interactive docs at http://127.0.0.1:8000/docs.

## Future Roadmap

The following features and improvements are planned to enhance the Options Intelligence Platform:

- **Implied Volatility Solver**  
  Implement a dedicated endpoint using numerical root-finding algorithms (e.g., Newton-Raphson) to derive implied volatility from observed market option prices.

- **Option Greeks Calculation**  
  Extend the C++ pricing engine to compute key Greeks — Delta, Gamma, Vega, Theta, and Rho — enabling comprehensive risk and sensitivity analysis.

- **Advanced Volatility Models**  
  Integrate stochastic volatility and local volatility models to improve pricing accuracy under complex market conditions.

- **Machine Learning Integration**  
  Develop ML models to predict volatility surfaces and option price movements, leveraging historical data and market features.

- **Expanded Contract Support**  
  Add support for exotic options and multi-asset derivatives to broaden platform applicability.

- **User Authentication & API Rate Limiting**  
  Implement secure user authentication and enforce rate limits for scalable and controlled API access.

- **Comprehensive Documentation & Tutorials**  
  Enhance documentation with detailed usage guides, API references, and example workflows.

- **Performance Optimization**  
  Profile and optimize both Python and C++ components to support ultra-low latency and high throughput.

- **Frontend Dashboard**  
  Build an interactive web dashboard to visualize option chains, volatility surfaces, and Greeks in real-time.
