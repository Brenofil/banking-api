# Banking API Documentation

Welcome to the Banking API documentation. This API provides comprehensive endpoints for managing users, accounts, transactions, and advanced document processing with table extraction capabilities.

## Quick Start

```bash
# Clone and navigate to project
cd banking-api

# Install dependencies
poetry install

# Configure environment
cp .env.example .env.local

# Start development server
poetry run uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

## Features

### Banking Operations
- User management (create, list, retrieve, delete)
- Account management with balance tracking
- Transaction processing (transfer, deposit, withdraw)

### Document Processing
- PDF upload and processing
- Automatic table extraction using Docling
- DataFrame conversion for data analysis
- Excel export with multiple sheets
- Support for password-protected PDFs

### API Features
- Interactive Swagger UI documentation
- Alternative ReDoc documentation
- CORS support for cross-origin requests
- Comprehensive error handling
- Structured response models

## Documentation Structure

### [About](about.md)
Overview of the Banking API, key features, and technologies used.

### [Architecture](architecture.md)
System design, project structure, design patterns, and data flow diagrams.

### [Endpoints](endpoints.md)
Complete API endpoint reference with request/response examples.

### [Configuration](configuration.md)
Environment variables, setup instructions, and deployment configuration.

## Quick Links

- **API Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## Example Usage

### Upload and Process a PDF

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Response

```json
{
  "status": "success",
  "data": {
    "tables": [...],
    "dataframes": [...],
    "excel_file": "files/document_20260415_120000_tables.xlsx"
  },
  "processing_time_ms": 1250.5,
  "page_count": 5,
  "confidence_score": 0.95
}
```

## Technology Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Docling** - Document processing
- **pandas** - Data analysis
- **Poetry** - Dependency management

## Requirements

- Python 3.11+
- Poetry for dependency management
- Optional: HuggingFace token for enhanced document processing

## Getting Help

- Check the [Configuration](configuration.md) guide for setup issues
- Review [Endpoints](endpoints.md) for API usage
- See [Architecture](architecture.md) for system design details

## License

This project is licensed under the Apache License 2.0.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This is a demonstration API using in-memory storage. For production use, integrate a proper database.
