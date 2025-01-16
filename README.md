# Product Recommendation Agent

A full-stack application built with Langgraph toolkit that provides intelligent product ordering and recommendation system. The project combines a robust backend powered by Langgraph with a modern Next.js frontend.

## Features

- **Modern Frontend**: Built with Next.js featuring a responsive and user-friendly interface
- **Robust Backend**: Powered by Langgraph toolkit for intelligent recommendation processing
- **API Integration**: RESTful API endpoints for seamless communication between frontend and backend
- **Component Library**: Custom UI components for consistent design
- **Natural Language Processing**: Converts natural language to SQL queries
- **Workflow Management**: Sophisticated node-based workflow system for handling recommendations
- **Database Integration**: SQL database integration for product data management

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/Vinci-virtuoso/Product-Recommendation-Agent.git
```

2. Install backend dependencies
```bash
poetry install
```
3. Configure database
```bash
cd src/app
python database.py
```
4. Move the .db file to root folder

5. Start the backend server
```bash
poetry run python main.py
```
6. Install frontend dependencies
```bash
cd frontend
npm install
```
7. Start the frontend development server
```bash
npm run dev
```

## Development

- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- API documentation available at `http://localhost:8000/docs`
