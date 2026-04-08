# Banking API

A simple banking data processment API built with FastAPI and Python 3. This API provides endpoints for managing users, accounts, and transactions.

## Features

- **User Management**: Create, list, retrieve, and delete users
- **Account Management**: Create accounts, check balances, and manage account details
- **Transaction Management**: Transfer money between accounts, deposit, and withdraw funds
- **Document Processing**: Upload and process documents with configurable file size limits
- **Interactive API Documentation**: Automatic Swagger UI and ReDoc documentation
- **CORS Support**: Configured for cross-origin requests

## Project Structure

```
banking-api/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic models (organized by domain)
│   │   ├── user.py          # User models
│   │   ├── account.py       # Account models
│   │   └── transaction.py   # Transaction models
│   └── routers/
│       ├── users.py         # User endpoints
│       ├── accounts.py      # Account endpoints
│       ├── transactions.py  # Transaction endpoints
│       └── documents.py    # Document processing endpoints
├── .env.example             # Environment variables template
├── pyproject.toml           # Poetry configuration and dependencies
├── poetry.lock              # Poetry lock file (auto-generated)
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) (Python dependency management tool)

### Installing Poetry

If you don't have Poetry installed, install it using one of these methods:

**On macOS/Linux/WSL:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**On Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Alternative (using pip):**
```bash
pip install poetry
```

For more installation options, visit: https://python-poetry.org/docs/#installation

### Setup

**IMPORTANT**: Poetry automatically creates and manages virtual environments for your project. This ensures dependency isolation and prevents conflicts with other Python projects.

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd banking-api
   ```

2. **Install dependencies** (Poetry will automatically create a virtual environment):
   ```bash
   poetry install
   ```

3. **Configure environment variables** (optional):
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to customize settings like `MAX_FILE_SIZE_MB` (default: 10 MB)

4. **Verify the virtual environment**:
   ```bash
   poetry env info
   ```
   This will show you the path to the virtual environment Poetry created.

### Virtual Environment Management

Poetry automatically manages virtual environments, but you can also:

- **Activate the virtual environment** (optional, for running commands directly):
  ```bash
  poetry shell
  ```

- **Run commands without activating** (recommended):
  ```bash
  poetry run <command>
  ```

- **Show virtual environment path**:
  ```bash
  poetry env info --path
  ```

- **List all virtual environments**:
  ```bash
  poetry env list
  ```

- **Remove the virtual environment**:
  ```bash
  poetry env remove python
  ```

## Running the API

Start the development server using Poetry:

```bash
poetry run uvicorn app.main:app --reload
```

**Alternative** (if you activated the virtual environment with `poetry shell`):
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Root & Health

- `GET /` - Welcome message and API information
- `GET /health` - Health check endpoint

### Document Processing (`/api/v1/processing`)

- `POST /api/v1/processing/upload` - Upload a document for processing
- `GET /api/v1/processing/config` - Get current processing configuration

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# Maximum file size for document uploads in megabytes
MAX_FILE_SIZE_MB=10
```

Available environment variables:
- `MAX_FILE_SIZE_MB`: Maximum file size for document uploads (default: 10 MB)

## Data Storage

**Note**: This is a demonstration API that uses in-memory storage. All data will be lost when the server restarts. For production use, you should integrate a proper database (PostgreSQL, MySQL, MongoDB, etc.).

## Development

### Adding New Dependencies

To add a new dependency:
```bash
poetry add <package-name>
```

To add a development dependency:
```bash
poetry add --group dev <package-name>
```

### Updating Dependencies

To update all dependencies:
```bash
poetry update
```

To update a specific dependency:
```bash
poetry update <package-name>
```

### Git Tagging Strategy

This project follows [Semantic Versioning](https://semver.org/) (SemVer) for version management.

#### Version Format: `vMAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes (e.g., v1.0.0 → v2.0.0)
- **MINOR**: New features, backward compatible (e.g., v1.0.0 → v1.1.0)
- **PATCH**: Bug fixes, backward compatible (e.g., v1.0.0 → v1.0.1)

#### Creating Tags

**1. Create an annotated tag** (recommended for releases):
```bash
git tag -a v0.2.0 -m "Release v0.0.0: Created the folder structure"
```

**2. Push the tag to remote**:
```bash
git push origin v0.0.0
```

**3. Push all tags**:
```bash
git push origin --tags
```

#### Tag Management Commands

```bash
git tag                         # list all tags

git tag -n                      # list tags with messages

git show v0.0.0                 # show tag details

git tag -d v0.0.0               # delete local tag

git push origin --delete v0.0.0 # delete remote tag

git checkout v0.2.0             # checkout a specific tag
```

#### Recommended Workflow

1. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "feat: add document processing endpoint"
   ```

2. **Update version in pyproject.toml**:
   ```toml
   [tool.poetry]
   version = "0.2.0"
   ```

3. **Create and push tag**:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0: Document processing and model refactoring"
   git push origin main
   git push origin v0.2.0
   ```

#### Version History

- **v0.0.0** - Initial release

#### Conventional Commits (Optional)

Consider using conventional commit messages for better changelog generation:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Example:
```bash
git commit -m "feat: add document upload with configurable size limit"
git commit -m "refactor: split models.py into separate domain files"
```

### Running Tests

(Tests not yet implemented - this is a basic example)

### Exporting Dependencies

If you need a `requirements.txt` file for deployment:
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Future Enhancements

- Add database integration (SQLAlchemy with PostgreSQL/MySQL)
- Implement authentication and authorization (JWT tokens)
- Add user password hashing
- Implement transaction history and filtering
- Add rate limiting
- Add comprehensive test suite
- Add logging and monitoring
- Implement account types with different rules
- Add currency conversion support
- Implement scheduled transactions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.