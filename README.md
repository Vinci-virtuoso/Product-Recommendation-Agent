# Product Recommendation Agent

This project implements a Python-based product recommendation and ordering agent for fashion items. 

**Functionality:** This agent allows users to interact with a fashion product database using natural language. It can understand questions about products, such as "show me all men's shoes," and process orders, like "order the Carlton London Women Stylish Black Flats." The agent converts these natural language queries into SQL commands, executes them against the database, and returns a human-readable response.

## Structure

*   `ProductRecommendation_agent.ipynb`: Core notebook for data analysis and model building.
*   `streamlit_app.py`: Streamlit app providing a user interface.
*   `fashion.csv`: Dataset of fashion items.
*   `.env`: Stores environment variables.
*   `example.db`: SQLite database for data storage.
*   `requirements.txt`: Lists project dependencies.

## Getting Started

To run the project:

1. Clone the repository.
2. Navigate to the project directory: `cd Product-Recommendation-Agent`
3. Create a virtual environment (optional): `python -m venv venv` and activate it.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the ProductRecommendation_agent down to the fastapi cell: `ProductRecommendation_agent.ipynb`
6. Run the Streamlit app: `streamlit run streamlit_app.py`

## Usage

Access the Streamlit app in your browser (usually `http://localhost:8501`) to interact with the product recommendation system.

## Future Enhancements

*   Enhance recommendation algorithms.
*   Expand the dataset.
*   Deploy to the cloud.
*   Implement user authentication.
*   Incorporate user feedback.
