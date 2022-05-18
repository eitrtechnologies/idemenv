async def test_unit_list_remote_empty(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No remote versions
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.list_remote = hub.idemenv.cli.list_remote

    # Mock fill_remote_version_list to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None

    # Set REMOTE_VERSIONS to be {}
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {}

    # Call list_remote
    await mock_hub.idemenv.cli.list_remote()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()


async def test_unit_list_remote_nonempty(mock_hub, hub, tmp_path, capfd):
    """
    SCENARIO #2:
    - There are remote versions
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.list_remote = hub.idemenv.cli.list_remote

    # Mock fill_remote_version_list to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None

    # Fill REMOTE_VERSIONS with two versions
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
    }

    # Call list_remote
    await mock_hub.idemenv.cli.list_remote()

    # Check that the expected list was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = "v18.7.0\nv18.6.1\nv18.5.0\nv18.4.2\nv18.4.1\nv18.4.0\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
