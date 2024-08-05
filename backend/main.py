from fastapi import FastAPI, Query


app = FastAPI()

@app.get("/{id}")
def read_root(id: int, language: str | None = Query(None)):
    return {
        "feature_enabled": False,
        "ab_test_flag": False
    }
