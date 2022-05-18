from unittest.mock import patch


async def test_func_pin_current_version_no_active_version(mock_hub, hub, tmp_path):
    """
    SCENARIO #1:
    - There is no active version
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.pin_current_version = hub.idemenv.ops.pin_current_version

    # Mock the return of get_current_version to be ("",""), meaning that
    # there is no active version
    mock_hub.idemenv.ops.get_current_version.return_value = ("", "")

    # Check that pin_current_version return False AND
    # that the override_version_file version IS NOT CHANGED
    with patch("os.getcwd") as mocked_override_dir:
        # Set up the mocked_override_file
        mocked_override_dir.return_value = tmp_path
        mocked_override_dir.mkdir()
        mocked_override_file = tmp_path / ".idem-version"
        existing_override_version = "v18.7.0"
        mocked_override_file.write_text("v18.7.0")

        # Confirm the return is False
        expected = False
        actual = await mock_hub.idemenv.ops.pin_current_version()
        actual == expected

        # Confirm that the mocked_override_file is unchanged
        assert mocked_override_file.read_text() == existing_override_version


async def test_func_pin_current_version_active_version_matches_override(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - There is an active version
    - The active version matches the version in the override file.
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.pin_current_version = hub.idemenv.ops.pin_current_version

    # Mock the return of get_current_version to be ("v18.7.0", tmp_path/version), where
    # tmp_path/version is the main version file. The main version file would have v18.7.0 as its value.
    existing_override_version = "v18.7.0"
    mock_hub.idemenv.ops.get_current_version.return_value = (
        existing_override_version,
        str(tmp_path / "version"),
    )

    # Check that pin_current_version return True AND that the
    # override_version_file version IS NOT CHANGED
    with patch("os.getcwd") as mocked_override_dir:
        # Set up the mocked_override_file
        mocked_override_dir.return_value = tmp_path
        mocked_override_dir.mkdir()
        mocked_override_file = tmp_path / ".idem-version"
        mocked_override_file.write_text(existing_override_version)

        # Confirm the return is True
        expected = True
        actual = await mock_hub.idemenv.ops.pin_current_version()
        assert actual == expected

        # Confirm that the mocked_override_file is unchanged
        assert mocked_override_file.read_text() == existing_override_version


async def test_func_pin_current_version_active_version_does_not_match_override(
    mock_hub, hub, tmp_path
):
    """
    SCENARIO #3:
    - There is an active version
    - The active version does not match the version in the override file.
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.pin_current_version = hub.idemenv.ops.pin_current_version

    # Mock the return of get_current_version to be ("v18.7.0", tmp_path/version), where
    # tmp_path/version is the main version file. The main version file would have v18.7.0 as its value.
    updated_override_version = "v18.7.0"
    mock_hub.idemenv.ops.get_current_version.return_value = (
        updated_override_version,
        str(tmp_path / "version"),
    )

    # Check that pin_current_version return True AND that the
    # override_version_file version IS CHANGED
    with patch("os.getcwd") as mocked_override_dir:
        # Set up the mocked_override_file
        mocked_override_dir.return_value = tmp_path
        mocked_override_dir.mkdir()
        mocked_override_file = tmp_path / ".idem-version"
        existing_override_version = "v18.6.1"
        mocked_override_file.write_text(existing_override_version)

        # Confirm the return is True
        expected = True
        actual = await mock_hub.idemenv.ops.pin_current_version()
        assert actual == expected

        # Confirm that the mocked_override_file is unchanged
        assert mocked_override_file.read_text() == updated_override_version
