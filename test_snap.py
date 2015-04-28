import os
import pytest
import re
import tempfile

from lib.util import command_check_error


@pytest.yield_fixture
def stderr_script():
    """Return the path to a script which outputs to stderr."""
    f, name = tempfile.mkstemp()
    os.write(f, b'#!/bin/bash\n/bin/echo "an error" >&2')
    os.close(f)
    os.chmod(name, 0o500)
    yield name
    os.unlink(name)

def test_command_check_error(stderr_script):
    # exit code 0 is NOT an error
    assert command_check_error('/bin/true') == None

    # a nonzero exit code is an error
    with pytest.raises(Exception) as excinfo:
        command_check_error('/bin/false')
    m = re.search('returned exit code (\d)', str(excinfo.value))
    assert int(m.groups()[0]) > 0

    # stderr output w/ fail_on_stderr == True (the default) is an error
    with pytest.raises(Exception) as excinfo:
        command_check_error(stderr_script)
    assert 'There was error output running' in str(excinfo.value)

    # stderr output w/ fail_on_stderr == False is NOT an error
    assert command_check_error(stderr_script, fail_on_stderr=False) == None
