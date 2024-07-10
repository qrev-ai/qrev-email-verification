import sys
from pathlib import Path

import pytest
from pi_conf import load_config
from qrev_cache.mongo_cache import Var, mongo_cache

from qrev_email_verification import InvalidEmailError, MVEmailResponse, MVMongoService

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # for conftest

from tests.services.conftest import MockVerifierMixin

load_config("qrev-ai-test").to_env()


class MockMongoService(MockVerifierMixin, MVMongoService):

    @mongo_cache(
        env_prefix="MILLIONVERIFIER_",
        query={
            "email": Var("email"),
            "service": "MillionVerifier",
        },
        data_type=MVEmailResponse,
        cache_only=True,
        skip_initial_verification=True,
    )
    def _get_email_response(self, email: str, **kwargs) -> MVEmailResponse:
        return super()._get_email_response(email, **kwargs)


@pytest.fixture
def service():
    return MockMongoService()  # type: ignore


def test_get_email_response_invalid1(service: MockMongoService):
    service.json_file = "invalid_example1.json"
    data = service.get_json()
    email = data["email"]
    ## assert error
    with pytest.raises(InvalidEmailError) as e:
        service.verify_email(email)


if __name__ == "__main__":
    pytest.main([__file__])
