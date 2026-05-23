"""
Main FastAPI application entry point
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents
from app.utils.logger import initialize_logger

app = FastAPI(
    title="Banking API",
    description="A simple banking API built with FastAPI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Initialize logger ONCE at startup
initialize_logger(
    log_dir=os.getenv("LOG_DIRECTORY", "logs"),
    log_level=os.getenv("LOG_LEVEL", "DEBUG"),
    rotation=os.getenv("LOG_ROTATION", "10 MB"),
    retention=os.getenv("LOG_RETENTION", "30 days"),
    compression=os.getenv("LOG_COMPRESSION", "zip"),
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
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Banking API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
