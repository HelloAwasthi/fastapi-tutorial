Social Feed & Voting API

A high-performance, modular RESTful backend built with FastAPI, PostgreSQL, and SQLAlchemy. The service provides complete CRUD workflows for posts, user management, stateless JWT authentication, resource ownership authorization, and a Reddit-style voting engine with aggregate vote counts.

Live Deployment & Interactive Docs

The backend is fully deployed and accessible in the cloud:

Live API Root: https://fastapi-tutorial-76vh.onrender.com/

Interactive Swagger UI Documentation: https://fastapi-tutorial-76vh.onrender.com/docs

Interactive ReDoc Documentation: https://fastapi-tutorial-76vh.onrender.com/redoc

Note on Free-Tier Hosting: Because the API is hosted on Render's free compute tier, the instance spins down during periods of inactivity. If testing the live link for the first time, please allow 30–50 seconds for the container to wake up.

Infrastructure & Cloud Architecture

API Hosting: Deployed on Render using an automated build pipeline running Uvicorn.

Database: Hosted on Neon, utilizing serverless managed PostgreSQL with connection pooling.

Security & Networking: Configured with custom CORS policies to selectively allow verified frontend origins.

Architecture & Engineering Highlights

Stateless Authentication: Implemented an OAuth2 password flow issuing signed JSON Web Tokens (JWT) with configurable expiration windows.

Cryptographic Security: Passwords are hashed using Passlib and Bcrypt with unique randomized salts; raw credentials are never persisted in PostgreSQL.

Fine-Grained Authorization: Ownership checks enforced at the database level on update and delete operations so users can modify only their own content.

Aggregations & Performance: Used SQLAlchemy LEFT OUTER JOIN alongside func.count and group_by to calculate vote totals directly inside the database in a single query, eliminating N+1 query bottlenecks.

Schema Isolation: Strictly separated incoming request validation from outbound response serialization using Pydantic schemas, guaranteeing password hashes and sensitive user metadata never leak into JSON responses.

Fail-Fast Configuration: Managed runtime secrets and database credentials through Pydantic BaseSettings, failing at boot if required environment variables are missing or misconfigured.

Tech Stack

Framework: FastAPI

Database: PostgreSQL (Neon Serverless)

ORM: SQLAlchemy

Data Validation: Pydantic v2

Authentication: Python-Jose (JWT), Passlib (Bcrypt)

Hosting / Cloud: Render, Neon

Database Schema

  +------------------+         +------------------+
  |      users       |         |      posts       |
  +------------------+         +------------------+
  | id (PK)          |<---+    | id (PK)          |<---+
  | email (Unique)   |    |    | title            |    |
  | password (Hash)  |    +----| owner_id (FK)    |    |
  | created_at       |         | content          |    |
  +------------------+         | published        |    |
           ^                   | created_at       |    |
           |                   +------------------+    |
           |                            ^              |
           |     +----------------+     |              |
           |     |     votes      |     |              |
           |     +----------------+     |              |
           +-----| user_id (PK,FK)|     |              |
                 | post_id (PK,FK)|-----+              |
                 +----------------+


API Endpoints

Authentication

POST /login - Authenticates user credentials via form-data and returns a Bearer JWT access token.

Users

POST /users/ - Registers a new user account with hashed password storage.

GET /users/{id} - Returns public profile details for a given user.

Posts

GET /posts/ - Retrieves paginated posts with aggregate vote counts. Supports query filters: limit, skip, and search.

POST /posts/ - Creates a new post attached to the authenticated user.

GET /posts/{id} - Retrieves a specific post by ID.

PUT /posts/{id} - Updates a post; restricted strictly to the post creator.

DELETE /posts/{id} - Deletes a post; restricted strictly to the post creator. Returns 204 No Content.

Votes

POST /vote/ - Toggles a like on a post (dir: 1 creates a vote, dir: 0 deletes an existing vote).

Environment Variables

To run this project locally or deploy it to a new environment, create a .env file in the project root:

DATABASE_HOSTNAME=ep-example.neon.tech
DATABASE_PORT=5432
DATABASE_PASSWORD=your_neon_password
DATABASE_NAME=neondb
DATABASE_USERNAME=your_neon_username
SECRET_KEY=your_generated_hex_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60


Local Setup & Development

1. Clone the repository

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


2. Set up a virtual environment

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt


4. Run the development server

uvicorn app.main:app --reload


The local API will be accessible at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.