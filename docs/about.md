# About the Banking API

A simple banking data processing API built with FastAPI and Python 3. This API provides comprehensive endpoints for managing users, accounts, transactions, and document processing with advanced table extraction capabilities.

## Overview

The Banking API is designed to demonstrate modern API development practices using FastAPI, with a focus on document processing and data extraction. The API includes sophisticated PDF processing capabilities that can extract tables and convert them to structured data formats.

## Key Features

### User & Account Management
- **User Management**: Create, list, retrieve, and delete users
- **Account Management**: Create accounts, check balances, and manage account details
- **Transaction Management**: Transfer money between accounts, deposit, and withdraw funds

### Document Processing
- **PDF Processing**: Upload and process PDF documents with advanced table extraction
- **Table Extraction**: Automatically extract tables from PDFs using Docling
- **DataFrame Conversion**: Convert extracted tables to pandas DataFrames
- **Excel Export**: Automatically export tables to Excel files with multiple sheets
- **Configurable Limits**: Adjustable file size limits via environment variables

### API Features
- **Interactive Documentation**: Automatic Swagger UI and ReDoc documentation
- **CORS Support**: Configured for cross-origin requests
- **Health Checks**: Built-in health check endpoints
- **Structured Responses**: Comprehensive response models with metadata

## Technologies

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

### Document Processing
- **Docling**: Advanced document processing and table extraction
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file generation
- **pikepdf**: PDF encryption/decryption support

### Development Tools
- **Poetry**: Dependency management and packaging
- **Python 3.11+**: Modern Python features and performance

## Data Storage

**Note**: This is a demonstration API that uses in-memory storage for user/account data. All data will be lost when the server restarts. For production use, integrate a proper database (PostgreSQL, MySQL, MongoDB, etc.).

Document processing results and exported files are persisted to the file system.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For detailed information, see:
- [Architecture](architecture.md) - System design and structure
- [Endpoints](endpoints.md) - API endpoints documentation
- [Configuration](configuration.md) - Environment and setup guide
