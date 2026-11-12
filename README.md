# Price-Mind-AI
A Python-based interactive web application designed to help users find the best tech devices (smartphones, tablets, smartwatches, laptops, headphones) at the best prices. The application scrapes real-time data from e-commerce platforms, stores it in a local database, and provides advanced filtering, smart scoring, and data visualization features.

📖 About the Application & How It Works

Smart Price Finder is a decision-support web application built to help users find the best tech devices within a specific budget, even when they do not have an exact product model in mind.

Here is how the system works behind the scenes:

Data Extraction: A web scraper (scraper.py) collects live product listings, prices, ratings, and technical specs from e-commerce websites.

Database & Price Tracking: Products are stored in a local SQLite database. Subsequent scraper runs update current prices and log any price changes into a dedicated price_history table, allowing users to track price drops over time.

Dual Search Modes: Users set a maximum budget and search either by exact product name (e.g., "iPhone 16", "Samsung Galaxy S25") or by technical parameters (category, brand, minimum memory, battery capacity, and 5G support).

Smart Scoring & Ranking: Matching products are evaluated and ranked using a custom weighted algorithm that outputs a score from 0 to 100:

40% Price Score: Rewards products that are well below the maximum budget.

30% Rating Score: Rewards highly-rated products.

30% Specification Score: Rewards products that match or exceed the user's technical requirements.

Visual Results: The top 6 highest-scoring products are displayed in a responsive 2-column grid. Each card features a 1–5 star rating, a direct store link, and an expandable price-history line chart. A market-wide Price vs. Rating scatter plot is also generated for broader analysis.

🌟 Key Features

Smart Budgeting: Automatically filters out products that exceed your financial constraints.

Automated Web Scraping: Extracts real-time pricing and specifications using BeautifulSoup and Requests.

Historical Price Tracking: Utilizes a custom UPSERT logic in SQLite to keep track of price fluctuations.

Interactive Dashboard: Built with Streamlit for a clean, modern, and user-friendly interface.

Data Visualization: Uses Pandas and Streamlit's native charting to generate scatter plots and line charts.

🛠️ Built With

Python 3.x

Streamlit (Frontend / UI Framework)

Pandas (Data manipulation and visualization)

Requests & BeautifulSoup4 (Web scraping)

SQLite3 (Database management)

📂 Project Structure

├── app.py                      # Main Streamlit web application
├── scraper.py                  # Web scraping script to fetch live data
├── requirements.txt            # Python dependencies
└── baza_de_date/
    ├── baza_de_date.py         # SQLite database creation and UPSERT logic
    └── products.db             # Local database file (generated automatically)


⚙️ Installation & Usage

1. Installation


# On Windows use: venv\Scripts\activate
# On Mac/Linux use: source venv/bin/activate


Install the required dependencies:

pip install -r requirements.txt


2. Running the Application

Step A: Populate the Database

Run the scraper first to fetch the latest products and prices from the web and save them to the local SQLite database.

python scraper.py


Step B: Start the Web Application

Run the Streamlit app to launch the user interface.

streamlit run app.py


Open your web browser and navigate to the local URL provided in the terminal (usually http://localhost:8501).

📈 Future Improvements

Integrate more e-commerce platforms for broader price comparison.

Add detailed CSV/Excel export functionality directly from the UI.

Implement asynchronous scraping to speed up data extraction.

Save user preferences and custom search filters between sessions.
