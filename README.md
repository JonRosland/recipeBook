# Recipe Book

A full-stack recipe management application with Deno frontend and Python backend.

## 📋 Features

- Store and manage your favorite recipes
- Search by ingredients or recipe name
- Responsive design for desktop and mobile
- Edit and add new recipes easily

## 🛠️ Technology Stack

- **Frontend**: Astro + Svelte with Deno runtime
- **Backend**: Python with Flask
- **Database**: MongoDB
- **Deployment**: Docker for easy local and production deployment

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Deno (for local development)
- Python 3.x (for local backend development)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/recipeBook.git
cd recipeBook
```

2. **Run with Docker (recommended)**

```bash
docker-compose up
```

The application will be available at:
- Frontend: http://localhost:8085
- Backend API: http://localhost:6088/api
- MongoDB Express (database admin): http://localhost:8081

### Local Development

#### Frontend (Deno + Astro)

```bash
cd frontend
yarn install
yarn dev
```

#### Backend (Python)

```bash
cd backend
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 📁 Project Structure

```
/
├── backend/                 # Python Flask backend
│   ├── api.py               # API routes and handlers
│   ├── main.py              # Entry point
│   ├── server.py            # Server configuration
│   └── requirements.txt     # Python dependencies
├── frontend/                # Astro + Svelte frontend
│   ├── src/
│   │   ├── components/      # Reusable Svelte components
│   │   ├── layouts/         # Page layouts
│   │   ├── pages/           # Astro pages
│   │   └── stores/          # State management
│   ├── public/              # Static assets
│   ├── astro.config.mjs     # Astro configuration
│   └── package.json         # Frontend dependencies
├── mongodb/                 # MongoDB data directory
└── docker-compose.yml       # Docker configuration
```

## 🧞 Commands

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `docker-compose up`       | Start the complete application stack             |
| `cd frontend && yarn dev` | Start frontend dev server at `localhost:4321`    |
| `cd frontend && yarn build` | Build frontend for production                  |
| `cd frontend && yarn preview` | Preview production build locally             |
| `cd backend && python main.py` | Start backend server at `localhost:6088`    |

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details