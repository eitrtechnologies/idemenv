from pathlib import Path
from unittest.mock import MagicMock


async def test_unit_install_empty_version_dicts(mock_hub, hub, capfd):
    """
    SCENARIO #1:
    - No local versions
    - No remote versions
    - Idem version is irrelevant
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.install = hub.idemenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Set the VERSIONS dicts to be {}
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {}

    # Mock the idem_version
    mock_hub.OPT.idemenv.idem_version = "v18.7.0"

    # Call install
    await mock_hub.idemenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"ERROR: {mock_hub.OPT.idemenv.idem_version} is not available as a binary.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.idemenv.ops.download_version.called


async def test_unit_install_nonempty_version_dicts_nonmatching_idem_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #2:
    - Local versions
    - Remote versions
    - Nonmatching idem version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.install = hub.idemenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Set the VERSIONS dicts to contain data
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
    }

    # Mock the idem_version to not match any entries in the VERSIONS dicts
    mock_hub.OPT.idemenv.idem_version = "nonexistent"

    # Call install
    await mock_hub.idemenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"ERROR: {mock_hub.OPT.idemenv.idem_version} is not available as a binary.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.idemenv.ops.download_version.called


async def test_unit_install_nonempty_local_empty_remote_matching_idem_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #3:
    - Local versions
    - No Remote versions
    - Matching idem version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.install = hub.idemenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to be nonempty
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }
    # Set the REMOTE_VERSIONS dict to be empty
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {}

    # Mock the idem_version to match an entry in the LOCAL_VERSIONS dict
    mock_hub.OPT.idemenv.idem_version = "v18.7.0"

    # Call install
    await mock_hub.idemenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.idemenv.idem_version} is already installed.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.idemenv.ops.download_version.called


async def test_unit_install_empty_local_nonempty_remote_matching_idem_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #4:
    - No Local versions
    - Remote versions
    - Matching idem version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.install = hub.idemenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Set the LOCAL_VERSIONS dict to be empty
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}
    # Set the REMOTE_VERSIONS dict to be nonempty
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
    }

    # Mock the idem_version to match an entry in the REMOTE_VERSIONS dict
    mock_hub.OPT.idemenv.idem_version = "v18.7.0"

    # Mock download_version to not do anything
    mock_hub.idemenv.ops.download_version.return_value = MagicMock()

    # Call install
    await mock_hub.idemenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = ""
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    mock_hub.idemenv.ops.download_version.assert_called_once_with("v18.7.0")


async def test_unit_install_nonempty_local_nonempty_remote_matching_idem_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #5:
    - Local versions
    - Remote versions
    - Matching idem version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.install = hub.idemenv.cli.install

    # Mock the fill functions to do nothing to do nothing
    mock_hub.idemenv.ops.fill_remote_version_list.return_value = None
    mock_hub.idemenv.ops.fill_local_version_list.return_value = None

    # Set the VERSION dicts to be nonempty
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path / "idem-v18.4.2"),
        "v18.7.0": Path(tmp_path / "idem-v18.7.0"),
    }
    mock_hub.idemenv.ops.REMOTE_VERSIONS = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
    }

    # Mock the idem_version to match an entry in both VERSION dicts
    mock_hub.OPT.idemenv.idem_version = "v18.7.0"

    # Mock download_version to not do anything (it should not be called, but just in case code is changed)
    mock_hub.idemenv.ops.download_version.return_value = MagicMock()

    # Call install
    await mock_hub.idemenv.cli.install()

    # Check that the expected output was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{mock_hub.OPT.idemenv.idem_version} is already installed.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_remote_version_list.assert_called_once()
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()
    assert not mock_hub.idemenv.ops.download_version.called
