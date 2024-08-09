import logging
import threading
import time
from typing import Any, Union
from fastapi import FastAPI, Query
from growthbook import GrowthBook, AbstractFeatureCache, feature_repo


class InMemoryStorageWithBackgroundReload(AbstractFeatureCache):
    def __init__(self) -> None:
        self.cache: dict[str, dict] = {}
        self.environment_data_polling_manager_thread = (
            FeaturesPollingManager(
                cache=self,
                refresh_interval_seconds=10,
                daemon=True,
            )
        )
        self.environment_data_polling_manager_thread.start()

    def get(self, key: str) -> dict | None:
        if key in self.cache:
            value = self.cache[key]
            return value
        return None

    def set(self, key: str, value: dict, ttl: int) -> None:
        self.cache[key] = value

    def clear(self) -> None:
        self.cache.clear()


class FeaturesPollingManager(threading.Thread):
    def __init__(
        self,
        *args: Any,
        cache: AbstractFeatureCache,
        refresh_interval_seconds: Union[int, float] = 10,
        **kwargs: Any,
    ):
        super(FeaturesPollingManager, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.cache = cache
        self.refresh_interval_seconds = refresh_interval_seconds
        self.api_host = "https://cdn.growthbook.io"
        self.client_key = "sdk-j3FK6hvlc58iloS"
        self.key = self.api_host + "::" + self.client_key

    def run(self) -> None:
        while not self._stop_event.is_set():
            features = feature_repo._fetch_features(
                api_host=self.api_host,
                client_key=self.client_key)
    
            if features:
                self.cache.set(self.key, features, -1)

            time.sleep(self.refresh_interval_seconds)

    def stop(self) -> None:
        self._stop_event.set()

    def __del__(self) -> None:
        self._stop_event.set()


# Configure GrowthBook to use your custom cache class
feature_repo.set_cache(InMemoryStorageWithBackgroundReload())


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
        on_experiment_viewed=on_experiment_viewed
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
