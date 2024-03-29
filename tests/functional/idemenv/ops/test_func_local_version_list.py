from pathlib import Path


async def test_func_local_version_list_nonexistent_dir(mock_hub, hub):
    """
    SCENARIO #1:
    - The versions directory does not exist
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.local_version_list = hub.idemenv.ops.local_version_list
    mock_hub.OPT.idemenv.idemenv_dir = "nonexistent_testing_dir"
    actual = await mock_hub.idemenv.ops.local_version_list()
    expected = {}
    assert expected == actual


async def test_func_local_version_list_existent_dir(mock_hub, hub, tmp_path):
    """
    SCENARIO #2:
    - The versions directory exists
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.local_version_list = hub.idemenv.ops.local_version_list
    mock_hub.OPT.idemenv.idemenv_dir = tmp_path

    # Create the mocked version dir to insert files in for testing
    mocked_versions_dir = tmp_path / "versions"
    mocked_versions_dir.mkdir()

    # Confirm that the return dictionary is empty if the directory does not contain any version files
    expected = {}
    actual = await mock_hub.idemenv.ops.local_version_list()
    assert actual == expected

    # Confirm that the return directory is correct when the directory contains valid and invalid version files
    # Create valid version files that will get picked up by the function
    valid_name_1 = "idem-v18.4.2"
    valid_path_1 = mocked_versions_dir / valid_name_1
    valid_path_1.write_text("valid")

    valid_name_2 = "idem-214"
    valid_path_2 = mocked_versions_dir / valid_name_2
    valid_path_2.write_text("valid")

    # Create invalid version files that will get picked up by the function
    invalid_name_1 = "idemv18.5.0"
    invalid_path_1 = mocked_versions_dir / invalid_name_1
    invalid_path_1.write_text("invalid")

    invalid_name_2 = "idm-v18.6.1"
    invalid_path_2 = mocked_versions_dir / invalid_name_2
    invalid_path_2.write_text("invalid")

    invalid_name_3 = "rand0m"
    invalid_path_3 = mocked_versions_dir / invalid_name_3
    invalid_path_3.write_text("invalid")

    # Compare the actual and expected results
    expected = {
        valid_name_1.replace("idem-", ""): Path(valid_path_1),
        valid_name_2.replace("idem-", ""): Path(valid_path_2),
    }
    actual = await mock_hub.idemenv.ops.local_version_list()
    assert expected == actual
