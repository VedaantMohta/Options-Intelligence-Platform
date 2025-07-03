# Options Intelligence Platform

![C++](https://img.shields.io/badge/C++-17-blue.svg) ![Python](https://img.shields.io/badge/Python-3.10+-blueviolet.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg) ![pybind11](https://img.shields.io/badge/pybind11-2.11-orange.svg)

A high-performance options analytics backend designed for quantitative analysis. This platform provides a RESTful API to fetch live option chain data from Polygon.io, price contracts using sophisticated C++ models, and generate interactive 3D pricing surfaces.

---

## Demo: Interactive 3D Pricing Surface

The platform's frontend can generate interactive 3D surface plots, visualizing an option's theoretical price (Z-axis) based on changes in the underlying stock price (X-axis) and time to maturity (Y-axis).
![image](https://github.com/user-attachments/assets/fb9768a5-c5a4-4e0e-9ff8-925f70852b2e)


---

## Key Features

-   **Live Option Chain Data**: Fetch real-time option contract data for any underlying stock, with filtering by contract type, expiration date, and strike price range.

-   **High-Performance Pricing Engine**: Core pricing models are written in modern C++17 for maximum performance and precision.
    -   **Binomial Tree Model**: Prices both American (early-exercise) and European options. Highly optimized with loop-invariant code hoisting to minimize branching in the hot path.
    -   **Black-Scholes Model**: A fast, analytical model for pricing European options, serving as a baseline for validation.

-   **Python-C++ Integration**: The C++ pricing engine is seamlessly exposed to Python using `pybind11`, combining C++ performance with Python's ease of use.

-   **Asynchronous REST API**: Built with FastAPI, the API is fully asynchronous, utilizing `httpx` for non-blocking I/O to handle high-concurrency workloads efficiently.

-   **On-the-Fly Volatility Estimation**: A dedicated service calculates annualized historical volatility from recent market data (since implied volatility was unavailable), providing a key input for pricing models.

-   **Interactive 3D Visualization**: An async endpoint coordinates over 400 C++ pricing evaluations to dynamically generate 3D data surfaces.

## Tech Stack

| Layer          | Technology                          | Purpose                                                      |
| :------------- | :---------------------------------- | :----------------------------------------------------------- |
| **Backend API**| Python (FastAPI)                    | Asynchronous request handling, data validation, and orchestration. |
| **Pricing Engine**| C++17                             | Performance-critical financial model calculations.           |
| **Integration**| `pybind11`                          | Creating efficient, low-overhead Python bindings for the C++ engine. |
| **Data Provider**| [Polygon.io](https://polygon.io/)   | Live market data for stock prices and option contracts.      |
| **Data Analysis**| `NumPy`                             | Numerical operations for volatility calculation.             |
| **HTTP Client**| `httpx`                             | High-performance, asynchronous HTTP requests to external APIs. |
| **Frontend** | React, Plotly.js, Tailwind CSS      | Interactive data visualization and user interface.           |

## System Architecture

The application is designed with a clear separation of concerns, ensuring modularity and scalability.

1.  **Frontend (React)**: The user interacts with a guided UI to select an option contract and trigger analysis.
2.  **API Layer (FastAPI)**: The frontend communicates with the backend via a RESTful API. Endpoints are validated using Pydantic schemas.
3.  **Service Layer (Python)**: The API calls dedicated `async` services to perform tasks.
    -   `Volatility Service`: Fetches historical price data to calculate `S` and `sigma`.
    -   `Options Service`: Fetches option chain and contract data from Polygon.io.
4.  **Pricing Engine (C++)**: For complex calculations like the heatmap, the service layer calls the compiled C++ module via its `pybind11` bridge, passing in market data to get a calculated price.
5.  **Response**: The priced data is structured and returned as JSON to the frontend for visualization.

## API Endpoints

A summary of the core API endpoints. For a full interactive list, run the server and navigate to `/docs`.

### `POST /options/heatmap`

Generates a 20x20 grid of theoretical option prices for a 3D surface plot.

-   **Request Body**:
    ```json
    {
      "ticker": "AAPL",
      "strike_price": 220,
      "expiration_date": "2025-09-19",
      "option_type": "call"
    }
    ```
-   **Response Body**:
    ```json
    {
      "stock_price_axis": [140.0, 146.6, ...],
      "time_axis": [250, 222, ...],
      "prices": [
        [5.50, 6.20, ...],
        [5.10, 5.75, ...],
        ...
      ]
    }
    ```

### `GET /options/strikes`

Fetches available strike prices for a given ticker and expiration date.

-   **Query Parameters**: `ticker` (str), `expiration_date` (str)
-   **Response Body**:
    ```json
    {
      "strikes": [210.0, 212.5, 215.0, 217.5, 220.0, ...]
    }
    ```

---

## Setup and Usage

### Prerequisites

-   Python 3.10+
-   A C++ compiler (MSVC for Windows, GCC/Clang for macOS/Linux)
-   Node.js and npm (for the frontend)
-   Git

### Backend Setup

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/VedaantMohta/options-intelligence-platform.git](https://github.com/VedaantMohta/options-intelligence-platform.git)
    cd options-intelligence-platform/backend
    ```

2.  **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key**:
    Create a `config.py` file in the `backend` directory:
    ```
    POLYGON_API_KEY = "your_polygon_api_key_here"
    ```

5.  **Compile the C++ Module**:
    ```bash
    python setup.py build_ext --inplace
    ```

6.  **Run the Backend Server (From Backend Directory)**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend is now running at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Navigate to Frontend Directory**:
    ```bash
    # From the root of the project
    cd frontend
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```

3.  **Run the Frontend Server**:
    ```bash
    npm run dev
    ```
    The frontend is now running at `http://localhost:5173` (or a similar port) and is proxied to the backend.

---

## Future Roadmap

-   [ ] **Implied Volatility Solver**: Implement a Newton-Raphson solver to calculate implied volatility from market prices.
-   [ ] **Greeks Calculation**: Extend the C++ engine to compute Delta, Gamma, Vega, and Theta for risk analysis.
-   [ ] **Advanced Volatility Models**: Integrate GARCH or other stochastic volatility models.
-   [ ] **User Authentication**: Implement JWT-based authentication for user accounts and saved settings.
-   [ ] **Containerization**: Dockerize the application for consistent deployment and scalability.
