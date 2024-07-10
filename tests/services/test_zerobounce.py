
import pytest
from pi_conf import load_config

from qrev_email_verification import InvalidEmailError, ZeroBounceService
from qrev_email_verification.services.zerobounce.models import ResultStatusEnum

## https://www.zerobounce.net/docs/email-validation-api-quickstart/#sandbox_mode__v2__

load_config("qrev-ai-test").to_env()


@pytest.fixture
def service():
    return ZeroBounceService()


## These are free api call emails from zerobounce
test_emails = [
    ("disposable@example.com", "invalid"),
    ("invalid@example.com", "invalid"),
    ("valid@example.com", "valid"),
    ("toxic@example.com", "invalid"),
    ("donotmail@example.com", "do_not_mail"),
    ("spamtrap@example.com", "spamtrap"),
    ("abuse@example.com", "abuse"),
    ("unknown@example.com", "unknown"),
    ("catch_all@example.com", "catch-all"),
    ("antispam_system@example.com", "invalid"),
    ("does_not_accept_mail@example.com", "invalid"),
    ("exception_occurred@example.com", "unknown"),
    ("failed_smtp_connection@example.com", "invalid"),
    ("failed_syntax_check@example.com", "invalid"),
    ("forcible_disconnect@example.com", "invalid"),
    ("global_suppression@example.com", "do_not_mail"),
    ("greylisted@example.com", "unknown"),
    ("leading_period_removed@example.com", "valid"),
    ("mail_server_did_not_respond@example.com", "unknown"),
    ("mail_server_temporary_error@example.com", "unknown"),
    ("mailbox_quota_exceeded@example.com", "invalid"),
    ("mailbox_not_found@example.com", "invalid"),
    ("no_dns_entries@example.com", "invalid"),
    ("possible_trap@example.com", "spamtrap"),
    ("possible_typo@example.com", "invalid"),
    ("role_based@example.com", "invalid"),
    ("timeout_exceeded@example.com", "unknown"),
    ("unroutable_ip_address@example.com", "invalid"),
    ("free_email@example.com", "valid"),
    ("role_based_catch_all@example.com", "do_not_mail"),
]


@pytest.mark.parametrize("email, category", test_emails)
def test_email_validation(service: ZeroBounceService, email: str, category):
    valids = set([ResultStatusEnum.VALID.value, ResultStatusEnum.CATCH_ALL.value])
    if category in valids:
        v = service.verify_email(email)
        assert v.status == category
    else:
        with pytest.raises(InvalidEmailError) as e:
            v = service.verify_email(email)
            assert v.email_response is not None  # type: ignore
            assert v._metadata is not None  # type: ignore


if __name__ == "__main__":
    pytest.main([__file__])
