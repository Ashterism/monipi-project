import pytest
import os, signal
from monipi.__main__ import sigterm_handler, exit_gracefully


def test_sigterm():
    with pytest.raises(SystemExit):
        os.kill(os.getpid(), signal.SIGTERM)

def test_exit_gracefully_basics():
    with pytest.raises(SystemExit):
        exit_gracefully()
