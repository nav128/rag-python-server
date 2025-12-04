from fastapi import HTTPException
import os
from typing import Optional

from fastapi import Header,Cookie


def get_api_key(
		x_api_key: Optional[str] = Header(None), 
		_x_api_key : Optional[str]=Cookie(None)
	) -> Optional[str]:
	"""Simple API key dependency.

	If WEATHER_API_KEY is set in the environment the incoming header must
	match it. If not set we allow any key (no-op) to simplify local dev.
	"""
	x_api_key = x_api_key or _x_api_key
	print(x_api_key)
	wanted = os.getenv("SERVER_API_KEY")
	if wanted:
		if not x_api_key or x_api_key != wanted:
			raise HTTPException(status_code=401, detail="invalid or missing API key")
	return x_api_key