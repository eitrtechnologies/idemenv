from pathlib import Path


async def test_func_remove_version_exists(mock_hub, hub, tmp_path):
    """
    SCENARIO #1:
    - The version exists within LOCAL_VERSIONS
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.remove_version = hub.idemenv.ops.remove_version

    # Create the new valid versions to include in LOCAL_VERSIONS
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()
    valid_path_old = mocked_versions_dir / "idem-v18.4.2"
    valid_path_old.write_text("valid")
    valid_path_new = mocked_versions_dir / "idem-v18.7.0"
    valid_path_new.write_text("valid")

    # Add the two valid versions to LOCAL_VERSIONS
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(valid_path_old),
        "v18.7.0": Path(valid_path_new),
    }

    # Set the expected LOCAL_VERSIONS value after remove_version is called.
    # This needs to be created before remove_version because otherwise
    # the Path object creation would fail due to the file having been deleted.
    expected_local_versions = {
        "v18.4.2": Path(valid_path_old),
        "v18.7.0": Path(valid_path_new),
    }

    # Call remove_version with a version that is present in LOCAL_VERSIONS
    ret = await mock_hub.idemenv.ops.remove_version("v18.7.0")
    assert ret == True

    # Confirm that the specified version had its file removed
    assert valid_path_new.exists() == False

    # Confirm that the LOCAL_VERSIONS list is unchanged.
    assert expected_local_versions == mock_hub.idemenv.ops.LOCAL_VERSIONS


async def test_func_remove_version_does_not_exist(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - The version does not exist within LOCAL_VERSIONS
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.remove_version = hub.idemenv.ops.remove_version

    # Create the new valid versions to include in LOCAL_VERSIONS
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()
    valid_path_old = mocked_versions_dir / "idem-v18.4.2"
    valid_path_old.write_text("valid")
    valid_path_new = mocked_versions_dir / "idem-v18.7.0"
    valid_path_new.write_text("valid")

    # Add the two valid versions to LOCAL_VERSIONS
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {
        "v18.4.2": Path(valid_path_old),
        "v18.7.0": Path(valid_path_new),
    }

    # Set the expected LOCAL_VERSIONS value after remove_version is called.
    expected_local_versions = {
        "v18.4.2": Path(valid_path_old),
        "v18.7.0": Path(valid_path_new),
    }

    # Call remove_version with a version that is not present in LOCAL_VERSIONS
    ret = await mock_hub.idemenv.ops.remove_version("v18.6.1")
    assert ret == True

    # Confirm that the two valid version files still exist and were unaffected by
    # the remove_version call
    assert valid_path_old.exists() == True
    assert valid_path_new.exists() == True

    # Confirm that the LOCAL_VERSIONS list is unchanged.
    assert expected_local_versions == mock_hub.idemenv.ops.LOCAL_VERSIONS


async def test_func_remove_version_empty_local_versions(mock_hub, hub):
    """
    SCENARIO #3:
    - LOCAL_VERSIONS is empty
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.remove_version = hub.idemenv.ops.remove_version

    # Set LOCAL_VERSIONS as empty
    mock_hub.idemenv.ops.LOCAL_VERSIONS = {}

    # Set the expected LOCAL_VERSIONS value after remove_version is called.
    expected_local_versions = {}

    # Call remove_version with a version that is not present in LOCAL_VERSIONS
    ret = await mock_hub.idemenv.ops.remove_version("v18.6.1")
    assert ret == True

    # Confirm that the LOCAL_VERSIONS list is unchanged.
    assert expected_local_versions == mock_hub.idemenv.ops.LOCAL_VERSIONS
