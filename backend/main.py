import logging
from fastapi import FastAPI, Query
from growthbook import GrowthBook


logging.basicConfig(level=logging.DEBUG)

def on_experiment_viewed(experiment, result):
  print("Viewed Experiment")
  print("Experiment Id: " + experiment.key)
  print("Variation Id: " + result.key)

app = FastAPI()

@app.get("/{id}")
def read_root(id: int, language: str | None = Query(None)):
    gb = GrowthBook(
        api_host="https://cdn.growthbook.io",
        client_key="sdk-j3FK6hvlc58iloS",
        on_experiment_viewed=on_experiment_viewed,
        cache_ttl=10
    )
    gb.load_features()
    gb.set_attributes({
        "id": id,
        "language": language
    })

    return {
        "feature_enabled": gb.is_on("my-cool-feature"),
        "ab_test_flag": False
    }
