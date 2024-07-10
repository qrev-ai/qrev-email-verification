import json
from typing import Any, Optional

import requests

from qrev_email_verification import APIResponse

example_dir = "tests/data/examples/millionverifier"

class MockVerifierMixin:
    def __init__(self, json_file: Optional[str] = None):
        self.json_file = json_file
        super().__init__()

    def get_json_file(self) -> str:
        assert self.json_file is not None
        if not self.json_file.startswith(example_dir):
            self.json_file = f"{example_dir}/{self.json_file}"
        return self.json_file

    def get_json(self) -> dict[str, Any]:
        assert self.json_file is not None
        with open(self.get_json_file()) as f:
            return json.load(f)

    def _get(self, url: str, params: dict[str, Any], **kwargs) -> APIResponse:
        r = requests.Response()
        r.status_code = 200
        mock_data = self.get_json()
        r._content = json.dumps(mock_data).encode(
            "utf-8"
        )  # Serialize mock_data to JSON and encode it
        r.headers["Content-Type"] = (
            "application/json"  # Optional: Set the content type to application/json
        )
        return APIResponse.from_response(r)
