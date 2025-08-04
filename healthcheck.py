from fastapi import FastAPI

app = FastAPI()

@app.head("/")
async def root():
    return Response(status_code=200)
