"""
    Routes for login
"""

from fastapi import routing, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any


router = routing.APIRouter(prefix="/authentication", tags=["authentication"])