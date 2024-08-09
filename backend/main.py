import json
import logging
from fastapi import FastAPI, Query
from growthbook import GrowthBook, AbstractFeatureCache, feature_repo
from redis import Redis


class RedisFeatureCache(AbstractFeatureCache):
  def __init__(self):
    self.r = Redis(host='redis', port=6379)
    self.prefix = "gb:"

  def get(self, key: str):
    data = self.r.get(self.prefix + key)
    # Data stored as a JSON string, parse into dict before returning
    return None if data is None else json.loads(data)

  def set(self, key: str, value: dict, ttl: int) -> None:
    self.r.set(self.prefix + key, json.dumps(value))
    self.r.expire(self.prefix + key, ttl)


# Configure GrowthBook to use your custom cache class
feature_repo.set_cache(RedisFeatureCache())


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
