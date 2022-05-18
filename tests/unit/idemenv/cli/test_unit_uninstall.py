from pathlib import Path


async def test_unit_uninstall_empty_local_versions(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No local versions
    - Idem version is irrelevant
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.uninstall = hub.idemenv.cli.uninstall

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to be {}
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}

    # Mock the idem_version
    mock_hub.OPT.idemenv.idem_version = "v18.7.0"

    # Call install
    await mock_hub.idemenv.cli.uninstall()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.idemenv.idem_version} is already uninstalled.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.idemenv.ops.remove_version.called


async def test_unit_uninstall_matching_idem_version(mock_hub, hub, capfd, tmp_path):
    """
    SCENARIO #2:
    - Local versions
    - Matching idem version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.uninstall = hub.idemenv.cli.uninstall

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to contain data
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }

    # Mock the idem_version
    mock_hub.OPT.idemenv.idem_version = "v18.7.0"

    # Mock remove_version to do nothing
    mock_hub.idemenv.ops.remove_version.return_value = None

    # Call install
    await mock_hub.idemenv.cli.uninstall()

    # Check that there was not output printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = ""
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.idemenv.ops.remove_version.assert_called_once()


async def test_unit_uninstall_nonmatching_idem_version(mock_hub, hub, capfd, tmp_path):
    """
    SCENARIO #3:
    - Local versions
    - Nonmatching idem version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.uninstall = hub.idemenv.cli.uninstall

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to contain data
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }

    # Mock the idem_version
    mock_hub.OPT.idemenv.idem_version = "v18.6.1"

    # Mock remove_version to do nothing
    mock_hub.idemenv.ops.remove_version.return_value = None

    # Call install
    await mock_hub.idemenv.cli.uninstall()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.idemenv.idem_version} is already uninstalled.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.idemenv.ops.remove_version.called
