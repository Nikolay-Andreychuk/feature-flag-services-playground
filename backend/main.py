from fastapi import FastAPI, Query
from UnleashClient import UnleashClient
from UnleashClient.cache import FileCache
from pathlib import Path

cache = FileCache("BootstrappedCache")
cache.bootstrap_from_file(Path("/app/flags.json"))
client = UnleashClient(
    url="http://host.docker.internal:4242/api/",
    app_name="playground",
    custom_headers={'Authorization': 'default:development.064b6f40e22f2f55a716667bf736ad2185a0831dded7a1de99ac33ac'},
    cache=cache,
    request_timeout=1,
    request_retries=0)

client.initialize_client()

app = FastAPI()

@app.get("/{id}")
def read_root(id: int, language: str | None = Query(None)):
    app_context = {
        "id": str(id),
        "language": language
    }
    
    return {
        "feature_enabled": client.is_enabled("my_cool_feature", app_context),
        "ab_test_flag": False
    }
