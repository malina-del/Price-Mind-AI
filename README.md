
# Price-Mind-AI

A Python-based interactive web application designed to help users find the best tech devices (smartphones, tablets, smartwatches, laptops, headphones) at the best prices. Whether users already know which product they want and are looking for the cheapest offer on the market, or they need help choosing the best device within a specific budget, Price-Mind-AI provides an intelligent way to compare products and make informed purchasing decisions.

The application collects product data from e-commerce platforms, stores it in a local database, and provides advanced filtering, smart scoring, and data visualization features.

## 📖 About the Application & How It Works

Price-Mind-AI is a decision-support web application designed to simplify the process of finding and comparing tech products.

It addresses two main user needs:

- **Exact Product Search:** Users who already know which product they want can search by its name and identify the cheapest available offer among the collected listings.
- **Smart Product Discovery:** Users who do not have a specific model in mind can set a budget and technical requirements to discover the best products that match their needs.

Here is how the system works behind the scenes:

**Data Extraction:** A web scraper (`scraper.py`) collects product listings, prices, ratings, and technical specifications from e-commerce websites.

**Database & Price Tracking:** Products are stored in a local SQLite database. Subsequent scraper runs update current prices and log any price changes into a dedicated `price_history` table, allowing users to track price fluctuations over time.

**Dual Search Modes:** Users can choose between two search modes:

- **Search by Product Name:** Search for a specific device (e.g., "iPhone 16", "Samsung Galaxy S25") to compare available offers and find the lowest price.
- **Search by Technical Parameters:** Set a maximum budget and filter products by category, brand, minimum memory, battery capacity, and 5G support to discover devices that match their requirements.

**Smart Scoring & Ranking:** Matching products are evaluated and ranked using a custom weighted algorithm that outputs a score from 0 to 100:

- 40% Price Score: Rewards products that are well below the maximum budget.
- 30% Rating Score: Rewards highly-rated products.
- 30% Specification Score: Rewards products that match or exceed the user's technical requirements.

The final score is calculated using the following formula:

`Final Score = (0.4 × Price Score) + (0.3 × Rating Score) + (0.3 × Specification Score)`

**Visual Results:** The top 6 highest-scoring products are displayed in a responsive 2-column grid. Each card features a 1–5 star rating, a direct store link, and an expandable price-history line chart. A market-wide Price vs. Rating scatter plot is also generated for broader analysis.

## 🌟 Key Features

- **Product Price Comparison:** Compare offers for a specific product and identify the lowest available price.
- **Smart Budgeting:** Discover products that fit within a specified budget and match technical requirements.
- **Automated Web Scraping:** Collects product prices and specifications using BeautifulSoup and Requests.
- **Historical Price Tracking:** Utilizes custom UPSERT logic in SQLite to keep track of price fluctuations.
- **Interactive Dashboard:** Built with Streamlit for a clean, modern, and user-friendly interface.
- **Data Visualization:** Uses Pandas and Streamlit's native charting to generate scatter plots and line charts.

## 🗄️ Database Structure

The application uses SQLite to store product information and track historical price changes.

- `products`: Stores product details, specifications, ratings, and current prices.
- `price_history`: Stores historical price records, allowing users to monitor price changes over time.

The database is updated using custom UPSERT logic to prevent duplicate product entries.

## 📸 Screenshots

Add screenshots of the application interface here.

## 🛠️ Built With

- **Python 3.x**
- **Streamlit** – Frontend / UI Framework
- **Pandas** – Data manipulation and visualization
- **Requests & BeautifulSoup4** – Web scraping
- **SQLite3** – Database management

## 📂 Project Structure

```text
Price-Mind-AI/
│
├── app.py                  # Main Streamlit web application
├── scraper.py              # Web scraping script to fetch product data
├── requirements.txt        # Python dependencies
│
└── baza_de_date/
    ├── baza_de_date.py     # SQLite database creation and UPSERT logic
    └── products.db         # Local database file (generated automatically)
```

## ⚙️ Installation & Usage

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Price-Mind-AI
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Running the Application

**Step A: Populate the Database**

Run the scraper first to fetch the latest products and prices from the web and save them to the local SQLite database.

```bash
python scraper.py
```

**Step B: Start the Web Application**

Run the Streamlit app to launch the user interface.

```bash
streamlit run app.py
```

Open your web browser and navigate to the local URL provided in the terminal (usually http://localhost:8501).

## 🧠 Technical Challenges

Some of the main challenges addressed during development include:

- Handling product data collected from different e-commerce websites.
- Extracting and organizing product specifications.
- Preventing duplicate records using SQLite UPSERT operations.
- Designing a weighted scoring algorithm to rank products.
- Tracking historical prices across multiple scraping sessions.

## 📈 Future Improvements

- Integrate more e-commerce platforms for broader price comparison.
- Add detailed CSV/Excel export functionality directly from the UI.
- Implement asynchronous scraping to speed up data extraction.
- Save user preferences and custom search filters between sessions.






