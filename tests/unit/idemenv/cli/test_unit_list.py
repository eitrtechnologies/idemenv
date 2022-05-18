from pathlib import Path


async def test_unit_list_no_local_no_current(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No local versions
    - No current version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.list = hub.idemenv.cli.list

    # Mock fill_local_version_list to do nothing
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Set LOCAL_VERSIONS to be {}
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}

    # Mock get_current_version to return no current version
    mock_hub.idemenv.ops.get_current_version.return_value = ("", "")

    # Call list
    await mock_hub.idemenv.cli.list()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.idemenv.ops.get_current_version.assert_called_once()


async def test_list_local_no_current(mock_hub, hub, tmp_path, capfd):
    """
    SCENARIO #2:
    - Two local versions
    - No current version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.list = hub.idemenv.cli.list

    # Mock fill_local_version_list to do nothing
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Fill LOCAL_VERSIONS with two versions
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }

    # Mock get_current_version to return no current version
    mock_hub.idemenv.ops.get_current_version.return_value = ("", "")

    # Call list
    await mock_hub.idemenv.cli.list()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "  v18.7.0\n  v18.4.2\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.idemenv.ops.get_current_version.assert_called_once()


async def test_list_local_current(mock_hub, hub, tmp_path, capfd):
    """
    SCENARIO #3:
    - Two local versions
    - A current version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.list = hub.idemenv.cli.list

    # Mock fill_local_version_list to do nothing
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Fill LOCAL_VERSIONS with two versions
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }

    # Mock get_current_version to return no current version
    mock_current_version_path = Path(tmp_path) / ".idem-version"
    mock_hub.idemenv.ops.get_current_version.return_value = ("v18.4.2", mock_current_version_path)

    # Call list
    await mock_hub.idemenv.cli.list()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"  v18.7.0\n* v18.4.2 (set by {mock_current_version_path})\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.idemenv.ops.get_current_version.assert_called_once()
