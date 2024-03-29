from unittest.mock import MagicMock
from unittest.mock import patch


async def test_unit_local_version_list_nonexistent_versions_dir(mock_hub, hub):
    """
    SCENARIO #1:
    - The versions_dir directory does not exist
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.local_version_list = hub.idemenv.ops.local_version_list

    # Rather than mock pathlib.Path, we will just set the mock_hub.OPT.idemenv.idemenv_dir
    # value because pathlib.Path is not easy to subclass for mocking purposes (issues occur
    # with the _flavour attribute)
    mock_hub.OPT.idemenv.idemenv_dir = "nonexistent_dir"

    # Mock Path.exists() to return False
    with patch("pathlib.PosixPath.exists", return_value=False) as mock_exists:
        # Ensure that an empty dict is returned
        actual = await mock_hub.idemenv.ops.local_version_list()
        expected = {}
        assert expected == actual

        # Ensure every mocked function was called the appropriate number of times
        mock_exists.assert_called_once()


async def test_unit_local_version_list_version_dir_exists_no_local_versions(
    mock_hub, hub, tmp_path
):
    """
    SCENARIO #2:
    - The versions_dir directory exists
    - There are no local versions matching the glob pattern
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.local_version_list = hub.idemenv.ops.local_version_list

    # Rather than mock pathlib.Path, we will just set the mock_hub.OPT.idemenv.idemenv_dir
    # value because pathlib.Path is not easy to subclass for mocking purposes (issues occur
    # with the _flavour attribute)
    mock_hub.OPT.idemenv.idemenv_dir = "existent_dir"

    # Mock Path.exists() to return True
    with patch("pathlib.PosixPath.exists", return_value=True) as mock_exists:
        # Mock Path.glob return an empty list
        glob_results = []
        with patch("pathlib.PosixPath.glob", return_value=glob_results) as mock_glob:
            # Ensure that an empty dict is returned
            actual = await mock_hub.idemenv.ops.local_version_list()
            expected = {}
            assert expected == actual

            # Ensure every mocked function was called the appropriate number of times
            mock_exists.assert_called_once()
            mock_glob.assert_called_once_with("idem-*")


async def test_unit_local_version_list_version_dir_exists_local_versions(mock_hub, hub, tmp_path):
    """
    SCENARIO #3:
    - The idemenv_dir directory exists
    - There are local versions matching the glob pattern
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.local_version_list = hub.idemenv.ops.local_version_list

    # Rather than mock pathlib.Path, we will just set the mock_hub.OPT.idemenv.idemenv_dir
    # value because pathlib.Path is not easy to subclass for mocking purposes (issues occur
    # with the _flavour attribute)
    mock_hub.OPT.idemenv.idemenv_dir = "existent_dir"

    # Mock Path.exists() to return True
    with patch("pathlib.PosixPath.exists", return_value=True) as mock_exists:

        # Mock Path.glob to return a list of Paths objects
        mocked_version_path1 = MagicMock()
        mocked_version_path1.name = "idem-v18.4.2"
        mocked_version_path2 = MagicMock()
        mocked_version_path2.name = "idem-v18.7.0"
        glob_results = [mocked_version_path1, mocked_version_path2]
        with patch("pathlib.PosixPath.glob", return_value=glob_results) as mock_glob:
            # Ensure that the dictionary contains keys for both the mocked versions
            actual = await mock_hub.idemenv.ops.local_version_list()
            expected = {"v18.4.2": mocked_version_path1, "v18.7.0": mocked_version_path2}
            assert expected == actual

            # Ensure every mocked function was called the appropriate number of times
            mock_exists.assert_called_once()
            mock_glob.assert_called_once_with("idem-*")
