async def test_unit_fill_remote_version_list(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.fill_remote_version_list = hub.idemenv.ops.fill_remote_version_list

    # Default REMOTE_VERSIONS to {}
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {}

    # Set the mocked return value of remote_version_list to be {}
    # and confirm that the remote_version_list value does not change
    mock_hub.idemenv.ops.remote_version_list.return_value = {}

    # Call fill_remote_version_list
    await mock_hub.idemenv.ops.fill_remote_version_list()

    # Confirm the value of REMOTE_VERSIONS matches our expected results
    expected = {}
    assert mock_hub.idemenv.ops.REMOTE_VERSIONS == expected

    # Now set the mocked return value to contain an element. This dictionary
    # with one element will be returned by remote_version_list and stored
    # within the REMOTE_VERSIONS dict
    mock_hub.idemenv.ops.remote_version_list.return_value = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
    }

    # Call fill_remote_version_list to populate the REMOTE_VERSIONS dict
    await mock_hub.idemenv.ops.fill_remote_version_list()

    # Confirm the value of REMOTE_VERSIONS matches our expected results
    expected = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
    }
    assert mock_hub.idemenv.ops.REMOTE_VERSIONS == expected
