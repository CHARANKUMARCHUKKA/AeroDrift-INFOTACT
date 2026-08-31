from fastapi import Request, HTTPException
import time

# Simple in-memory rate limiter for MVP
RATE_LIMIT = 100 # requests
RATE_WINDOW = 60 # seconds
clients = {}

async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    if client_ip not in clients:
        clients[client_ip] = []
        
    clients[client_ip] = [t for t in clients[client_ip] if now - t < RATE_WINDOW]
    
    if len(clients[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")
        
    clients[client_ip].append(now)
    response = await call_next(request)
    return response
