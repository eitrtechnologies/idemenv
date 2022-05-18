from pathlib import Path


async def test_unit_version_exists(mock_hub, hub, capfd, tmp_path):
    """
    SCENARIO #1:
    - There is a current version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.version = hub.idemenv.cli.version

    # Mock the get_current_version function to return a mock version
    mock_curr_version = ("v18.4.2", Path(tmp_path) / "v18.4.2")
    mock_hub.idemenv.ops.get_current_version.return_value = mock_curr_version

    # Call version
    await mock_hub.idemenv.cli.version()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_curr_version[0]} (set by {mock_curr_version[1]})\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.get_current_version.assert_called_once_with()


async def test_unit_version_nonexistent(mock_hub, hub, capfd):
    """
    SCENARIO #2:
    - There is not a current version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.version = hub.idemenv.cli.version

    # Mock the get_current_version function to return a mock version
    mock_curr_version = ("", "")
    mock_hub.idemenv.ops.get_current_version.return_value = mock_curr_version

    # Call version
    await mock_hub.idemenv.cli.version()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "ERROR: No version of Idem is set!\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.get_current_version.assert_called_once_with()
