from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import aiofiles
from aiofiles import threadpool


async def test_unit_use_version_no_local_version_nonexistent_version(
    mock_hub, hub, tmp_path, capfd
):
    """
    SCENARIO #1:
    - No local versions
    - A version that does not exist was specified
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.use_version = hub.idemenv.ops.use_version

    # Set LOCAL_VERSIONS as an empty dict
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}

    # Mock the fill_local_version_list function so it returns an empty list
    mock_hub.idemenv.ops.fill_local_version_list.return_value = []

    # Call use_version and confirm it passed successfully
    version = "v18.4.2"
    actual_ret = await mock_hub.idemenv.ops.use_version(version)
    actual_ret == True

    # Check that the expected warning was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{version} is not installed. Run 'idemenv install {version}' first.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_local_version_list.assert_called_once()


async def test_unit_use_version_local_versions_nonexistent_version(mock_hub, hub, tmp_path, capfd):
    """
    SCENARIO #2:
    - There are local versions
    - A version that does not exist was specified
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.use_version = hub.idemenv.ops.use_version

    # Set LOCAL_VERSIONS to contain two versions
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path) / "idem-v18.4.2",
        "v18.7.0": Path(tmp_path) / "idem-v18.7.0",
    }

    # Call use_version and confirm it passed successfully
    version = "v18.6.1"
    actual_ret = await mock_hub.idemenv.ops.use_version(version)
    actual_ret == True

    # Check that the expected warning was printed
    actual_stdout, err = capfd.readouterr()
    expected_stdout = f"{version} is not installed. Run 'idemenv install {version}' first.\n"
    assert actual_stdout == expected_stdout

    # Ensure every mocked function was called the appropriate number of times
    mock_hub.idemenv.ops.fill_local_version_list.assert_not_called()


async def test_unit_use_version_local_versions_existent_version(mock_hub, hub, tmp_path):
    """
    SCENARIO #3:
    - There are local versions
    - A version that exists is specified
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.use_version = hub.idemenv.ops.use_version

    # Set LOCAL_VERSIONS to contain two versions
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(tmp_path) / "idem-v18.4.2",
        "v18.7.0": Path(tmp_path) / "idem-v18.7.0",
    }

    # Set the idemenv_dir value as the mock directory
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path

    # Patch mkdir to do nothing
    with patch("pathlib.PosixPath.mkdir", return_value=None) as mock_mkdir:

        # Register the return type with aiofiles.threadpool.wrap dispatcher
        aiofiles.threadpool.wrap.register(MagicMock)(
            lambda *args, **kwargs: threadpool.AsyncBufferedIOBase(*args, **kwargs)
        )

        # Mock the file returned by aiofiles.open
        mock_version_file = MagicMock()
        with patch("aiofiles.threadpool.sync_open", return_value=mock_version_file) as mock_open:
            mock_version_file.write.side_effect = None

            # Call use_version and confirm it passed successfully
            version = "v18.7.0"
            actual_ret = await mock_hub.idemenv.ops.use_version(version)
            actual_ret == True

            # Ensure every mocked function was called the appropriate number of times
            mock_hub.idemenv.ops.fill_local_version_list.assert_not_called()
            mock_mkdir.assert_called_once()
            mock_open.assert_called_once()
            mock_mkdir.assert_called_once()
            mock_version_file.write.assert_called_once()
