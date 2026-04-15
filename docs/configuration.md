# Configuration

Complete guide for configuring the Banking API.

## Environment Variables

The API uses environment variables for configuration. Create a `.env` file in the project root (copy from `.env.example`).

### Available Variables

#### LOG_LEVEL
```bash
LOG_LEVEL="INFO"
```

**Description**: Sets the logging level for the application.

**Options**:
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

**Default**: `INFO`

#### MAX_FILE_SIZE_MB
```bash
MAX_FILE_SIZE_MB=10
```

**Description**: Maximum file size for document uploads in megabytes.

**Type**: Integer

**Default**: `10` (10 MB)

**Example**:
```bash
MAX_FILE_SIZE_MB=50  # Allow up to 50 MB files
```

#### HF_TOKEN
```bash
HF_TOKEN=your_huggingface_token_here
```

**Description**: HuggingFace Hub token for authenticated API requests.

**Purpose**:
- Enables higher rate limits
- Faster model downloads
- Access to gated models

**How to get**:
1. Create a free account at [huggingface.co](https://huggingface.co/)
2. Go to [Settings → Tokens](https://huggingface.co/settings/tokens)
3. Create a new token (read access is sufficient)
4. Add it to your `.env` file

**Note**: Without this token, you'll see warnings about unauthenticated requests and may experience rate limits.

#### FILE_LOCATION
```bash
FILE_LOCATION=files
```

**Description**: Directory for storing exported files (Excel, CSV, etc.).

**Type**: String (directory path)

**Default**: `files` (if not set)

**Behavior**:
- Directory is created automatically if it doesn't exist
- Can be absolute or relative path
- Relative paths are relative to project root

**Examples**:
```bash
FILE_LOCATION=files                    # Default
FILE_LOCATION=/var/app/exports         # Absolute path
FILE_LOCATION=exports/documents        # Nested directory
```

## Configuration File

### .env.example

Template file with all available configuration options:

```bash
LOG_LEVEL="INFO"

# Maximum file size for document uploads in megabytes
MAX_FILE_SIZE_MB=10

# HuggingFace Hub token for authenticated requests
# Get your token from: https://huggingface.co/settings/tokens
# This enables higher rate limits and faster model downloads
HF_TOKEN=your_huggingface_token_here

# Directory for storing exported files (Excel, CSV, etc.)
FILE_LOCATION=files
```

### .env.local

Your local configuration file (not tracked by git):

```bash
# Copy from .env.example and customize
cp .env.example .env.local
```

**Important**: `.env.local` is in `.gitignore` to prevent committing sensitive data.

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Configure Environment

```bash
# Copy example configuration
cp .env.example .env.local

# Edit configuration
nano .env.local  # or use your preferred editor
```

### 3. Set HuggingFace Token (Recommended)

```bash
# Add your token to .env.local
HF_TOKEN=hf_your_actual_token_here
```

### 4. Verify Configuration

```bash
# Check Poetry environment
poetry env info

# Test configuration
poetry run python -c "import os; print('LOG_LEVEL:', os.getenv('LOG_LEVEL', 'INFO'))"
```

## Running the API

### Development Server

```bash
# Start with auto-reload
poetry run uvicorn app.main:app --reload

# Custom host and port
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# With specific log level
LOG_LEVEL=DEBUG poetry run uvicorn app.main:app --reload
```

### Production Server

```bash
# Production mode (no reload)
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## File Storage Configuration

### Default Behavior

If `FILE_LOCATION` is not set:
1. System checks for environment variable
2. Falls back to `files` directory
3. Creates directory if it doesn't exist

### Custom Location

```bash
# Set custom location
FILE_LOCATION=/var/app/exports

# Or in code
from app.utils.file_operations import FileOperations

file_ops = FileOperations(base_directory="/custom/path")
```

### Directory Structure

```
files/
├── document1_20260415_120000_tables.xlsx
├── document2_20260415_120100_tables.xlsx
└── document3_20260415_120200_tables.xlsx
```

Files are named with pattern: `{original_name}_{timestamp}_tables.xlsx`

## Logging Configuration

### Log Levels

```bash
# Development
LOG_LEVEL=DEBUG

# Production
LOG_LEVEL=INFO

# Troubleshooting
LOG_LEVEL=WARNING
```

### Log Output

Logs are written to:
- Console (stdout)
- `logs/` directory (if configured)

### Log Format

```
2026-04-15 12:00:00 | INFO | Component | module:function:line - Message
```

## CORS Configuration

CORS is configured in [`main.py`](../app/main.py):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Restrict `allow_origins` to specific domains.

## API Documentation

### Swagger UI
- URL: `http://localhost:8000/docs`
- Interactive API testing
- Request/response examples

### ReDoc
- URL: `http://localhost:8000/redoc`
- Alternative documentation view
- Better for reading

## Performance Tuning

### File Size Limits

```bash
# Increase for large documents
MAX_FILE_SIZE_MB=50

# Decrease for resource-constrained environments
MAX_FILE_SIZE_MB=5
```

### Worker Processes

```bash
# More workers for better concurrency
poetry run uvicorn app.main:app --workers 8

# Recommended: 2-4 workers per CPU core
```

### Memory Considerations

- Large PDFs require more memory
- Adjust `MAX_FILE_SIZE_MB` based on available RAM
- Monitor memory usage in production

## Security Configuration

### Environment Variables

**Never commit**:
- `.env.local`
- `.env`
- Any file with actual tokens/secrets

**Always commit**:
- `.env.example` (with placeholder values)

### File Permissions

```bash
# Secure configuration files
chmod 600 .env.local

# Secure export directory
chmod 755 files/
```

### Production Checklist

- [ ] Set strong `HF_TOKEN`
- [ ] Configure specific CORS origins
- [ ] Set appropriate `MAX_FILE_SIZE_MB`
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Enable logging
- [ ] Regular security updates

## Troubleshooting

### Common Issues

#### HuggingFace Warnings

**Problem**: Warnings about unauthenticated requests

**Solution**: Set `HF_TOKEN` in `.env.local`

#### File Upload Fails

**Problem**: `413 Payload Too Large`

**Solution**: Increase `MAX_FILE_SIZE_MB`

#### Directory Not Found

**Problem**: Cannot write to `FILE_LOCATION`

**Solution**: Check directory permissions or let system create it automatically

#### Import Errors

**Problem**: Module not found errors

**Solution**: 
```bash
poetry install
poetry run python your_script.py
```

## Environment-Specific Configuration

### Development

```bash
LOG_LEVEL=DEBUG
MAX_FILE_SIZE_MB=10
FILE_LOCATION=files
```

### Staging

```bash
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=25
FILE_LOCATION=/var/app/staging/exports
```

### Production

```bash
LOG_LEVEL=WARNING
MAX_FILE_SIZE_MB=50
FILE_LOCATION=/var/app/production/exports
HF_TOKEN=<production_token>
```

## Additional Resources

- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [HuggingFace Tokens](https://huggingface.co/docs/hub/security-tokens)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)