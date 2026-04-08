# Banking API

A simple banking API built with FastAPI and Python 3. This API provides endpoints for managing users, accounts, and transactions.

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
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic models (organized by domain)
│   │   ├── __init__.py
│   │   ├── user.py          # User models
│   │   ├── account.py       # Account models
│   │   └── transaction.py   # Transaction models
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User endpoints
│       ├── accounts.py      # Account endpoints
│       ├── transactions.py  # Transaction endpoints
│       └── processing.py    # Document processing endpoints
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

### Users (`/api/v1/users`)

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get a specific user
- `DELETE /api/v1/users/{user_id}` - Delete a user

### Accounts (`/api/v1/accounts`)

- `POST /api/v1/accounts/` - Create a new account
- `GET /api/v1/accounts/` - List all accounts (optional: filter by user_id)
- `GET /api/v1/accounts/{account_id}` - Get a specific account
- `GET /api/v1/accounts/{account_id}/balance` - Get account balance
- `DELETE /api/v1/accounts/{account_id}` - Delete an account

### Transactions (`/api/v1/transactions`)

- `POST /api/v1/transactions/` - Create a transfer between accounts
- `POST /api/v1/transactions/deposit` - Deposit money into an account
- `POST /api/v1/transactions/withdraw` - Withdraw money from an account
- `GET /api/v1/transactions/` - List all transactions (optional: filter by account_id)
- `GET /api/v1/transactions/{transaction_id}` - Get a specific transaction

### Document Processing (`/api/v1/processing`)

- `POST /api/v1/processing/upload` - Upload a document for processing
- `GET /api/v1/processing/config` - Get current processing configuration

## Example Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "password": "securepassword"
  }'
```

### Create an Account

```bash
curl -X POST "http://localhost:8000/api/v1/accounts/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "account_type": "checking",
    "currency": "USD"
  }'
```

### Deposit Money

```bash
curl -X POST "http://localhost:8000/api/v1/transactions/deposit" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 1,
    "amount": 1000.00,
    "description": "Initial deposit"
  }'
```

### Transfer Money

```bash
curl -X POST "http://localhost:8000/api/v1/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "from_account_id": 1,
    "to_account_id": 2,
    "amount": 100.00,
    "description": "Payment"
  }'
```

### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/processing/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

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
git tag -a v0.2.0 -m "Release v0.2.0: Added document processing and refactored models"
```

**2. Push the tag to remote**:
```bash
git push origin v0.2.0
```

**3. Push all tags**:
```bash
git push origin --tags
```

#### Tag Management Commands

**List all tags**:
```bash
git tag
```

**List tags with messages**:
```bash
git tag -n
```

**Show tag details**:
```bash
git show v0.2.0
```

**Delete a local tag**:
```bash
git tag -d v0.2.0
```

**Delete a remote tag**:
```bash
git push origin --delete v0.2.0
```

**Checkout a specific tag**:
```bash
git checkout v0.2.0
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

- **v0.1.0** - Initial release with user, account, and transaction management
- **v0.2.0** - Added document processing endpoint and refactored models into separate files

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

### Code Style

The code follows PEP 8 style guidelines.

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