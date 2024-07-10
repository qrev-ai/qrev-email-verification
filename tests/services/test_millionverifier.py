import sys
from pathlib import Path

import pytest
from pi_conf import load_config

from qrev_email_verification import InvalidEmailError, MillionVerifierService

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # for testing when in vscode

from tests.services.conftest import MockVerifierMixin

load_config("qrev-ai-test").to_env()


class MockVerifierService(MockVerifierMixin, MillionVerifierService):
    pass

@pytest.fixture
def service():
    return MockVerifierService()

def test_get_email_response_invalid1(service: MockVerifierService):
    service.json_file = "invalid_example1.json"
    data = service.get_json()
    email = data["email"]
    ## assert error
    with pytest.raises(InvalidEmailError) as e:
        service.verify_email(email)


if __name__ == "__main__":
    pytest.main([__file__])
