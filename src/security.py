from fastapi import HTTPException
import os
from typing import Optional
import logging

from fastapi import Header,Cookie
logger = logging.getLogger(__name__)

def get_api_key(
		x_api_key: Optional[str] = Header(None), 
	) -> Optional[str]:
	"""Simple API key dependency.

	If WEATHER_API_KEY is set in the environment the incoming header must
	match it. If not set we allow any key (no-op) to simplify local dev.
	"""
	wanted = os.getenv("SERVER_API_KEY")
	if wanted:
		if not x_api_key or x_api_key != wanted:
			raise HTTPException(status_code=401, detail="invalid or missing API key")
	return x_api_key