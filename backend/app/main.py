from fastapi import FastAPI

app = FastAPI(title="Healthcare AI Agent API")


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
