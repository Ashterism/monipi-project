import pytest
import os, signal
from monipi.runner import sigterm_handler


def test_sigterm():
    with pytest.raises(SystemExit):
        os.kill(os.getpid(), signal.SIGTERM)
