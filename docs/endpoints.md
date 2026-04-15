# API Endpoints

Complete reference for all API endpoints available in the Banking API.

## Base URL

- **Development**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## Root & Health Endpoints

### Welcome Message
```
GET /
```

Returns welcome message and API information.

**Response:**
```json
{
  "message": "Welcome to Banking API",
  "version": "0.0.0",
  "docs": "/docs"
}
```

### Health Check
```
GET /health
```

Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "healthy"
}
```

## Document Processing Endpoints

Base path: `/api/v1/documents`

### Upload Document
```
POST /api/v1/documents/upload
```

Upload and process a document (PDF) with automatic table extraction and Excel export.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): Document file to upload
  - `password` (optional): Password for encrypted/protected PDFs

**Response:** `ProcessorResponse`
```json
{
  "status": "success",
  "data": {
    "text": "Extracted text content...",
    "tables": [
      {
        "index": 0,
        "data": {...},
        "rows": 5,
        "columns": 4
      }
    ],
    "dataframes": [
      {
        "data": [
          {"col1": "val1", "col2": "val2"},
          ...
        ],
        "columns": ["col1", "col2"],
        "shape": [5, 4],
        "index": [0, 1, 2, 3, 4]
      }
    ],
    "excel_file": "files/document_20260415_120000_tables.xlsx",
    "metadata": {...}
  },
  "processor_type": "pdf",
  "processing_time_ms": 1250.5,
  "extracted_text": "Full text...",
  "page_count": 5,
  "tables": [...],
  "images": [...],
  "confidence_score": 0.95,
  "processed_at": "2026-04-15T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Document processed successfully
- `400 Bad Request`: Invalid file or parameters
- `413 Payload Too Large`: File exceeds size limit
- `500 Internal Server Error`: Processing failed

**Features:**
- Automatic table extraction from PDFs
- DataFrame conversion with smart column handling
- Excel file export with multiple sheets
- Support for password-protected PDFs
- Comprehensive metadata extraction

### Get Processing Configuration
```
GET /api/v1/documents/config
```

Get current document processing configuration.

**Response:**
```json
{
  "max_file_size_mb": 10,
  "max_file_size_bytes": 10485760
}
```

## User Management Endpoints

Base path: `/api/v1/users`

### Create User
```
POST /api/v1/users
```

Create a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "cpf": "123.456.789-00"
}
```

**Response:** `User`

### List Users
```
GET /api/v1/users
```

Get list of all users.

**Response:** `List[User]`

### Get User
```
GET /api/v1/users/{user_id}
```

Get specific user by ID.

**Response:** `User`

### Delete User
```
DELETE /api/v1/users/{user_id}
```

Delete a user.

**Response:** Success message

## Account Management Endpoints

Base path: `/api/v1/accounts`

### Create Account
```
POST /api/v1/accounts
```

Create a new account for a user.

**Request Body:**
```json
{
  "user_id": 1,
  "initial_balance": 1000.00
}
```

**Response:** `Account`

### Get Account
```
GET /api/v1/accounts/{account_id}
```

Get specific account by ID.

**Response:** `Account`

### Get Balance
```
GET /api/v1/accounts/{account_id}/balance
```

Get current account balance.

**Response:**
```json
{
  "account_id": 1,
  "balance": 1000.00
}
```

## Transaction Endpoints

Base path: `/api/v1/transactions`

### Transfer Money
```
POST /api/v1/transactions/transfer
```

Transfer money between accounts.

**Request Body:**
```json
{
  "from_account_id": 1,
  "to_account_id": 2,
  "amount": 100.00
}
```

**Response:** `Transaction`

### Deposit
```
POST /api/v1/transactions/deposit
```

Deposit money into an account.

**Request Body:**
```json
{
  "account_id": 1,
  "amount": 500.00
}
```

**Response:** `Transaction`

### Withdraw
```
POST /api/v1/transactions/withdraw
```

Withdraw money from an account.

**Request Body:**
```json
{
  "account_id": 1,
  "amount": 200.00
}
```

**Response:** `Transaction`

### Get Transaction
```
GET /api/v1/transactions/{transaction_id}
```

Get specific transaction by ID.

**Response:** `Transaction`

## Response Models

### ProcessorResponse

Complete response from document processing operations.

**Fields:**
- `status`: Processing status (success, failed, partial_success, etc.)
- `data`: Extracted structured data including tables and dataframes
- `metadata`: Document metadata (page count, author, etc.)
- `processor_type`: Type of processor used (e.g., "pdf")
- `processing_time_ms`: Processing duration in milliseconds
- `extracted_text`: Raw text extracted from document
- `page_count`: Number of pages in document
- `tables`: List of extracted tables
- `images`: Information about images in document
- `errors`: List of error messages (if any)
- `warnings`: List of warning messages (if any)
- `confidence_score`: Extraction confidence (0.0 to 1.0)
- `processed_at`: Timestamp of processing

### User

User model.

**Fields:**
- `id`: User ID
- `name`: User name
- `email`: Email address
- `cpf`: Brazilian tax ID

### Account

Account model.

**Fields:**
- `id`: Account ID
- `user_id`: Owner user ID
- `balance`: Current balance
- `created_at`: Creation timestamp

### Transaction

Transaction model.

**Fields:**
- `id`: Transaction ID
- `from_account_id`: Source account ID
- `to_account_id`: Destination account ID
- `amount`: Transaction amount
- `type`: Transaction type (transfer, deposit, withdraw)
- `timestamp`: Transaction timestamp

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `400 Bad Request`: Invalid input or parameters
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File size exceeds limit
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server-side error

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

## Authentication

Currently, no authentication is required. For production use, implement JWT-based authentication or similar security measures.