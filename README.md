# Product Recommendation Agent

A full-stack application built with Langgraph toolkit that provides intelligent product recommendations. The project combines a robust backend powered by Langgraph with a modern Next.js frontend.

## Project Structure

```
Langgraph-toolkit/
├── frontend/
│   ├── app/
│   │   ├── fonts/
│   │   ├── favicon.ico
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── hooks/
│   │   │   │   └── use-toast.ts
│   │   │   └── ui/
│   │   │       ├── button.tsx
│   │   │       ├── form.tsx
│   │   │       ├── input.tsx
│   │   │       ├── label.tsx
│   │   │       └── toast.tsx
│   │   └── lib/
│   │       └── utils.ts
├── src/
│   └── app/
│       ├── api/
│       │   └── v1/
│       │       ├── endpoints/
│       │       │   └── __init__.py
│       │       └── __init__.py
│       ├── logic/
│       │   ├── check_attempts_router.py
│       │   ├── execute_sql_router.py
│       │   ├── get_database_schema.py
│       │   ├── relevance_router.py
│       │   └── __init__.py
│       ├── models/
│       │   ├── chat_models.py
│       │   └── __init__.py
│       ├── nodes_and_edges/
│       │   ├── nodes/
│       │   │   ├── check_relevance.py
│       │   │   ├── convert_nl_sql.py
│       │   │   ├── end_max_iterations.py
│       │   │   ├── execute_sql.py
│       │   │   ├── get_current_user.py
│       │   │   ├── human_readable_answer.py
│       │   │   ├── irrelevant.py
│       │   │   ├── regenerate_query.py
│       │   │   └── __init__.py
│       │   └── __init__.py
│       ├── states/
│       ├── test/
│       ├── workflows/
│       └── __init__.py
├── example.db
├── main.py
├── mermaid.py
├── poetry.lock
└── pyproject.toml
```

## Features

- **Modern Frontend**: Built with Next.js featuring a responsive and user-friendly interface
- **Robust Backend**: Powered by Langgraph toolkit for intelligent recommendation processing
- **API Integration**: RESTful API endpoints for seamless communication between frontend and backend
- **Component Library**: Custom UI components for consistent design
- **Natural Language Processing**: Converts natural language to SQL queries
- **Workflow Management**: Sophisticated node-based workflow system for handling recommendations
- **Database Integration**: SQL database integration for product data management

## Technology Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- Custom UI Components

### Backend
- Python
- Langgraph Toolkit
- FastAPI
- SQL Database
- Poetry for dependency management

## Project Components

### Frontend Structure
- **Components**: Reusable UI components including forms, buttons, and toasts
- **Hooks**: Custom React hooks for state management
- **Layout**: Base layout and page components
- **Utils**: Utility functions and helpers

### Backend Structure
- **API**: Versioned API endpoints (v1)
- **Logic**: Core business logic including SQL execution and relevance checking
- **Models**: Data models and chat models
- **Nodes**: Individual processing nodes for the recommendation workflow
  - Query conversion
  - Relevance checking
  - SQL execution
  - Answer generation
- **States**: State management for the workflow
- **Tests**: Testing suite

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/Vinci-virtuoso/Product-Recommendation-Agent.git
```

2. Install backend dependencies
```bash
poetry install
```

3. Install frontend dependencies
```bash
cd frontend
npm install
```

4. Start the backend server
```bash
poetry run python main.py
```

5. Start the frontend development server
```bash
cd frontend
npm run dev
```

## Development

- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- API documentation available at `http://localhost:8000/docs`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.