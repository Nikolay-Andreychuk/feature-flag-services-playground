import os
from fastapi import FastAPI, Query
from flagsmith import Flagsmith
from flagsmith.offline_handlers import LocalFileHandler


local_file_handler = LocalFileHandler(environment_document_path="/app/flags.json")
flagsmith = Flagsmith(
    environment_key=os.getenv("FLAGSMITH_API_KEY"),
    enable_local_evaluation=True,
    offline_handler=local_file_handler)

app = FastAPI()

@app.get("/{id}")
def read_root(id: int, language: str | None = Query(None)):
    traits = {"language": language}
    identity_flags = flagsmith.get_identity_flags(identifier=str(id), traits=traits)
    return {
        "feature_enabled": identity_flags.is_feature_enabled("my_cool_feature"),
        "ab_test_flag": identity_flags.get_feature_value("my_cool_ab_test"),
    }
