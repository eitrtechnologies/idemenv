from pathlib import Path
from unittest import mock

import aiofiles


async def test_func_use_version_no_local_version_nonexistent_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #1:
    - No local versions
    - A version that does not exist was specified
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.use_version = hub.idemenv.ops.use_version

    # Mock the fill_local_version_list function so it does not do anything
    mock_hub.idemenv.ops.fill_local_version_list.return_value = mock.MagicMock()

    # Set up the mocked versions directory
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()

    # Set LOCAL_VERSIONS as an empty dict
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}

    # Call use_version and confirm it passed successfully
    version = "v18.4.2"
    actual_ret = await mock_hub.idemenv.ops.use_version(version)
    actual_ret == True

    # Check that the expected warning was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{version} is not installed. Run 'idemenv install {version}' first.\n"
    assert actual_stdout == expected_stdout

    # Confirm that fill_local_version_list was called once because LOCAL_VERSIONS
    # is empty.
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()


async def test_func_use_version_local_versions_nonexistent_version(mock_hub, hub, tmp_path, capfd):
    """
    SCENARIO #2:
    - There are local versions
    - A version that does not exist was specified
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.use_version = hub.idemenv.ops.use_version

    # Mock the fill_local_version_list function so it does not do anything.
    # However, it should not be called at all (tested below)
    mock_hub.idemenv.ops.fill_local_version_list.return_value = mock.MagicMock()

    # Set up the mocked versions directory
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()

    # Create the two version files to include in LOCAL_VERSIONS
    valid_path_old = mocked_versions_dir / "idem-v18.4.2"
    valid_path_old.write_text("valid")

    valid_path_new = mocked_versions_dir / "idem-v18.7.0"
    valid_path_new.write_text("valid")

    # Set LOCAL_VERSIONS to contain two versions
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(valid_path_old),
        "v18.7.0": Path(valid_path_new),
    }

    # Call use_version and confirm it passed successfully
    version = "v18.6.1"
    actual_ret = await mock_hub.idemenv.ops.use_version(version)
    actual_ret == True

    # Confirm that fill_local_version_list was not ever called
    assert not mock_hub.idemenv.ops.fill_local_version_list.called

    # Check that the expected warning was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{version} is not installed. Run 'idemenv install {version}' first.\n"
    assert actual_stdout == expected_stdout


async def test_func_use_version_local_versions_existent_version(mock_hub, hub, tmp_path):
    """
    SCENARIO #3:
    - There are local versions
    - A version that exists is specified
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.use_version = hub.idemenv.ops.use_version

    # Mock the fill_local_version_list function so it does not do anything.
    # However, it should not be called at all (tested below)
    mock_hub.idemenv.ops.fill_local_version_list.return_value = mock.MagicMock()

    # Set up the mocked versions file and directory
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path
    # File
    mocked_version_file = tmp_path / "version"
    mocked_version_file.write_text("")
    # Directory
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()

    # Create the two version files to include in LOCAL_VERSIONS
    valid_path_old = mocked_versions_dir / "idem-v18.4.2"
    valid_path_old.write_text("")

    valid_path_new = mocked_versions_dir / "idem-v18.7.0"
    valid_path_new.write_text("")

    # Set LOCAL_VERSIONS to contain two versions
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(valid_path_old),
        "v18.7.0": Path(valid_path_new),
    }

    # Call use_version and confirm it passed successfully
    version = "v18.7.0"
    actual_ret = await mock_hub.idemenv.ops.use_version(version)
    actual_ret == True

    # Confirm that fill_local_version_list was not ever called
    assert not mock_hub.idemenv.ops.fill_local_version_list.called

    # Confirm that the version file now has the correct version specified
    actual_vfile_contents = None
    async with aiofiles.open(mocked_version_file, "r") as vfile:
        actual_vfile_contents = await vfile.read()
    assert actual_vfile_contents == version
