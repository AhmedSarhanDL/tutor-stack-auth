from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginData):
    # Dummy login for now
    if data.username == "test" and data.password == "test":
        return {"access_token": "dummy_token", "token_type": "bearer"}
    return {"detail": "Invalid credentials"} 