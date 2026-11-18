# Price-Mind-AI 🔎

A Python-based interactive web application designed to help users find the best tech devices (smartphones, tablets, smartwatches, laptops, headphones) at competitive prices. Whether users already know which product they want and are looking for the best available offer, or they need help choosing the best device within a specific budget, **Price-Mind-AI** provides an intelligent way to compare products and make informed purchasing decisions.

The application collects product data from e-commerce platforms, stores it in a local database, and provides advanced filtering, smart scoring, and data visualization features.

## 📖 About the Application & How It Works

Price-Mind-AI is a decision-support web application designed to simplify the process of finding and comparing tech products.

It addresses two main user needs:

- **Exact Product Search:** Users who already know which product they want can search by its name and compare matching offers within their selected budget. Products are ranked according to their overall score, which considers price and rating.
- **Smart Product Discovery:** Users who do not have a specific model in mind can set a budget and technical requirements to discover products that match their needs.

### How the Application Works

**1. Data Extraction**

A web scraper (`scraper.py`) collects product listings, prices, ratings, images, and product links from eight supported e-commerce websites.

**2. Database & Price Tracking**

Products are stored in a local SQLite database. Subsequent scraper runs update product information and record price changes in a dedicated `price_history` table, allowing users to monitor price fluctuations over time.

**3. Dual Search Modes**

Users can choose between two search modes:

- **Search by Product Name:** Search for a specific device (e.g., "iPhone 16", "Samsung Galaxy S25") to find matching products and compare their prices and ratings.
- **Search by Technical Parameters:** Set a maximum budget and filter products by category, brand, minimum memory, battery capacity, and 5G support to discover devices that match their requirements.

**4. Smart Scoring & Ranking**

Matching products are evaluated and ranked using a custom weighted algorithm that outputs a score from 0 to 100:

- **40% Price Score:** Rewards products that are priced well below the maximum budget.
- **30% Rating Score:** Rewards highly-rated products.
- **30% Specification Score:** Rewards products that match the selected technical requirements.

The final score is calculated using the following formula:

`Final Score = (0.4 × Price Score) + (0.3 × Rating Score) + (0.3 × Specification Score)`

Products are sorted in descending order according to their overall score.

**5. Visual Results & Product Navigation**

After entering the search criteria, the application displays up to six products that best match the user's requirements.

The results are presented in a responsive two-column layout.

Each product card displays relevant information, including:

- Product name and image.
- Product brand.
- Product rating and star score.
- Product price.
- Overall ranking score.
- A direct link to the original online store page.
- An expandable price-history section, when historical data is available.

By clicking the product link, users can access the store's website, find additional product information, and proceed with their purchase.

**6. Data Visualization**

The application generates a Price vs. Rating scatter plot, allowing users to compare products based on their prices and ratings.

Additionally, each product can include an expandable price-history line chart, helping users understand how its price has changed over time.

## 🌟 Key Features

- **Product Price Comparison:** Compare offers for a specific product across collected listings.
- **Smart Budgeting:** Discover products that fit within a specified budget and match technical requirements.
- **Automated Web Scraping:** Collect product prices, ratings, images, and product information from eight supported online stores.
- **Historical Price Tracking:** Uses SQLite to store historical price records and monitor price fluctuations.
- **Interactive Dashboard:** Built with Streamlit for a clean and user-friendly interface.
- **Top 6 Recommendations:** Displays up to six products matching the search criteria, ranked by their overall score.
- **Smart Product Matching:** Supports direct and approximate text matching when searching by product name.
- **Product Ratings:** Displays product ratings and star scores. When a store does not provide rating information, the scraper may use a default rating.
- **Technical Filtering:** Filter products by category, brand, memory, battery capacity, and 5G support.
- **Direct Store Access:** Open the original product page directly from the application.
- **Data Visualization:** Uses Pandas and Streamlit's charting capabilities to generate scatter plots and line charts.

## 🗄️ Database Structure

The application uses SQLite to store product information and track historical price changes.

- `products`: Stores product details, specifications, ratings, images, links, and current prices.
- `price_history`: Stores historical price records, allowing users to monitor price changes over time.

The database uses custom UPSERT logic to update existing product records and avoid unnecessary duplicate entries.

## 📸 Screenshots

<img width="1850" height="1006" alt="image" src="https://github.com/user-attachments/assets/8b0eecf6-ab92-443e-aee2-21c1439585e5" />

<img width="1818" height="918" alt="image" src="https://github.com/user-attachments/assets/cb07d90c-7427-4922-afa4-46c2b6e1a99c" />

<img width="1833" height="908" alt="image" src="https://github.com/user-attachments/assets/23d28278-83ce-4808-ba77-5bf0692ea890" />

<img width="1795" height="986" alt="image" src="https://github.com/user-attachments/assets/61b5f857-4e94-4758-95cf-aa8ba9bc4fa2" />

<img width="1762" height="549" alt="image" src="https://github.com/user-attachments/assets/f1432672-b668-405b-b297-6867a79b3ac0" />

## 🛠️ Built With

- **Python 3.x**
- **Streamlit** – Frontend / UI Framework.
- **Pandas** – Data manipulation and visualization.
- **Requests & BeautifulSoup4** – Web scraping.
- **SQLite3** – Database management.
- **difflib** – Approximate text matching for product searches.

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
    └── products.db         # Local database file
```

## ⚙️ Installation & Usage

To run Price-Mind-AI locally, follow these steps.

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Price-Mind-AI
```

### 2. Create and Activate a Virtual Environment

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

### 3. Install the Required Dependencies

Install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

These dependencies allow the application to process product information, interact with the database, collect online product data, and display the web interface.

### 4. Populate the Database

Run the scraper to collect product information and prices from supported e-commerce websites:

```bash
python scraper.py
```

The collected information is processed and stored in the local SQLite database.

### 5. Run the Application

After the database has been populated, start the Streamlit application:

```bash
python -m streamlit run app.py
```

Once the command is executed, the application interface will open in your web browser.

### 6. Using the Application

Once the interface is open, users can follow these steps:

1. **Enter a Maximum Budget:** Set the maximum amount they are willing to spend.
2. **Choose a Search Mode:** Select either Exact Product Search or Smart Product Discovery.
3. **Enter Search Criteria:**
   - If the exact product is known, enter its name.
   - If the exact model is unknown, select the desired technical parameters.
4. **View Recommendations:** The application displays up to six products that match the selected criteria.
5. **Compare Products:** Check product prices, ratings, brands, and overall scores.
6. **Explore Charts:** Analyze the Price vs. Rating chart and available historical price information.
7. **Export Results:** Download the displayed product results as a CSV file.
8. **Visit the Online Store:** Click the product link to access its original page and find additional product information.

## 🧠 Technical Challenges

Some of the main challenges addressed during development include:

- Handling product data collected from different e-commerce websites.
- Extracting and organizing product information from HTML and structured JSON-LD data.
- Identifying product brands, memory capacities, and connectivity features from product titles.
- Handling missing rating information through default values.
- Designing a weighted scoring algorithm to rank products.
- Preventing duplicate records using SQLite UPSERT operations.
- Tracking historical prices across multiple scraping sessions.
- Implementing approximate text matching for product searches.
- Combining product filtering, price comparison, and ratings into a single interactive interface.

## 📈 Future Improvements

- Integrate more e-commerce platforms for broader price comparison.
- Improve the extraction of technical specifications, including actual battery capacities.
- Retrieve more accurate product ratings from all supported stores.
- Implement pagination or navigation arrows to browse more than six results.
- Add Excel export functionality alongside the existing CSV export.
- Implement asynchronous scraping to speed up data extraction.
- Save user preferences and custom search filters between sessions.
- Expand product categories and technical filtering options.
- Improve price comparison and historical price analysis.

---

**Price-Mind-AI** combines web scraping, database management, product filtering, ranking algorithms, and data visualization to help users discover suitable electronic devices and compare available offers before making a purchase.





