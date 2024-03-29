from pathlib import Path
from unittest import mock


async def test_func_get_current_version_both_files_dont_exist(mock_hub, hub):
    """
    SCENARIO #1
    - override_version_file DOES NOT EXIST
    - main_version_file DOES NOT EXIST
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.get_current_version = hub.idemenv.ops.get_current_version

    # Set the idemenv_dir as a nonexistent directory
    mock_hub.OPT.idemenv.idemenv_dir = "nonexistent_testing_dir"

    # Patch os.getcwd() to be a nonexistent directory
    with mock.patch("os.getcwd") as mocked_override_dir:
        mocked_override_dir.return_value = "nonexistent_testing_dir"
        expected = ("", "")
        actual = await mock_hub.idemenv.ops.get_current_version()
        actual == expected


async def test_func_get_current_version_only_override_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #2
    - override_version_file DOES EXIST
    - main_version_file DOES NOT EXIST
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.get_current_version = hub.idemenv.ops.get_current_version

    # Mock the idemenv_dir to be a nonexistent dir (so the file does not exist)
    mock_hub.OPT.idemenv.idemenv_dir = "nonexistent_testing_dir"

    with mock.patch("os.getcwd") as mocked_override_dir:
        # Mock the os.getcwd() return to be tmp_path
        mocked_override_dir.return_value = tmp_path
        mocked_override_dir.mkdir()
        mocked_override_file = tmp_path / ".idem-version"
        version = "v18.7.0"
        mocked_override_file.write_text(version)

        # Get the results of get_current_version
        actual = await mock_hub.idemenv.ops.get_current_version()
        expected = (version, str(mocked_override_file))

        # Confirm that the actual and expected results match
        assert actual == expected


async def test_func_get_current_version_only_main_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #3
    - override_version_file DOES NOT EXIST
    - main_version_file DOES EXIST
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.get_current_version = hub.idemenv.ops.get_current_version

    # Mock the idemenv_dir to be an existing mocked dir
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path

    # Create the mocked main_version_file with a version of v18.6.1
    mocked_main_version_file = Path(mock_hub.OPT.idemenv.idemenv_dir) / "version"
    version = "v18.6.1"
    mocked_main_version_file.write_text(version)

    with mock.patch("os.getcwd") as mocked_override_dir:
        # Mock the os.getcwd() return to be an empty dirtectory that
        # does not contain the .idem-version file
        mocked_override_dir.return_value = "empty_testing_dir"
        mocked_override_dir.mkdir()

        # Get the results of get_current_version
        actual = await mock_hub.idemenv.ops.get_current_version()
        expected = (version, str(mocked_main_version_file))

        # Confirm that the actual and expected results match
        assert actual == expected


async def test_func_get_current_version_both_files_exist(mock_hub, hub, tmp_path):
    """
    SCENARIO #4
    - override_version_file DOES EXIST
    - main_version_file DOES EXIST
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.get_current_version = hub.idemenv.ops.get_current_version

    # Mock the idemenv_dir to be an existing mocked dir
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path

    # Create the mocked main_version_file with a version of v18.6.1
    mocked_main_version_file = Path(mock_hub.OPT.idemenv.idemenv_dir) / "version"
    main_version = "v18.6.1"
    mocked_main_version_file.write_text(main_version)

    with mock.patch("os.getcwd") as mocked_override_dir:
        # Mock the os.getcwd() return to be tmp_path
        mocked_override_dir.return_value = tmp_path
        mocked_override_dir.mkdir()
        mocked_override_file = tmp_path / ".idem-version"
        override_version = "v18.7.0"
        mocked_override_file.write_text(override_version)

        # Get the results of get_current_version
        actual = await mock_hub.idemenv.ops.get_current_version()
        expected = (override_version, str(mocked_override_file))

        # Confirm that the actual and expected results match
        assert actual == expected
