"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import accounts, transactions, users, documents

app = FastAPI(
    title="Banking API",
    description="A simple banking API built with FastAPI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["accounts"])
# app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Banking API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


