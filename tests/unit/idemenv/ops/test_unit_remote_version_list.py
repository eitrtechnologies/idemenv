async def test_unit_remote_version_list_valid_response(mock_hub, hub):
    """
    SCENARIO #1:
    - There was a valid response recieved by the GET request
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.remote_version_list = hub.idemenv.ops.remote_version_list

    # Set the return value of the mocked hub.exec.request.raw.get to be a valid return object.
    # Note: Only the some of the dictionary values are included in this mocked return object.
    # This is because many values are not necessary from a testing perspective.
    mock_hub.exec.request.raw.get.return_value = {
        "result": True,
        "ret": b"""
        <html><body><pre>
            <a href="../">../</a>
            <a href="latest/">latest/</a>
            <a href="v18.4.0-3/">v18.4.0-3/</a>
            <a href="v18.4.0-4/">v18.4.0-4/</a>
            <a href="v18.4.1/">v18.4.1/</a>
            <a href="v18.4.2-2/">v18.4.2-2/</a>
            <a href="v18.4.2/">v18.4.2/</a>
            <a href="v18.5.0/">v18.5.0/</a>
            <a href="v18.6.1/">v18.6.1/</a>
            <a href="v18.7.0/">v18.7.0/</a>
        </pre></body></html>
        """,
        "comment": "OK",
        "ref": "exec.request.raw.get",
        "status": 200,
    }

    # Compare the actual and expected results
    expected = {
        "v18.4.0": "v18.4.0-4",
        "v18.4.1": "v18.4.1",
        "v18.4.2": "v18.4.2",
        "v18.5.0": "v18.5.0",
        "v18.6.1": "v18.6.1",
        "v18.7.0": "v18.7.0",
        "latest": "latest",
    }
    actual = await mock_hub.idemenv.ops.remote_version_list()
    assert expected == actual


async def test_unit_remote_version_list_invalid_response_no_ret(mock_hub, hub):
    """
    SCENARIO #2:
    - There was a invalid response received by the GET request (no "ret" value)
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.remote_version_list = hub.idemenv.ops.remote_version_list

    # Set the return value of the mocked hub.exec.request.raw.get to be an invalid return object.
    # Note: Only the some of the dictionary values are included in this mocked return object.
    # This is because many values are not necessary from a testing perspective.
    mock_hub.exec.request.raw.get.return_value = {
        "result": True,
        "comment": "OK",
        "ref": "exec.request.raw.get",
        "status": 200,
    }

    # Compare the actual and expected results
    expected = {}
    actual = await mock_hub.idemenv.ops.remote_version_list()
    assert expected == actual


async def test_unit_remote_version_list_invalid_status_code_response(mock_hub, hub):
    """
    SCENARIO #2:
    - There was a invalid response received by the GET request (Actual error such as 404 -- Bad Response)
    """
    # Link the function to the mock_hub
    mock_hub.idemenv.ops.remote_version_list = hub.idemenv.ops.remote_version_list

    # Set the return value of the mocked hub.exec.request.raw.get to be an invalid return object.
    # Note: Only the some of the dictionary values are included in this mocked return object.
    # This is because many values are not necessary from a testing perspective.
    mock_hub.exec.request.raw.get.return_value = {
        "result": False,
        "ret": "An incorrect query parameter was specified",
        "comment": "Not Found",
        "ref": "exec.request.raw.get",
        "status": 404,
        "headers": {},
    }

    # Compare the actual and expected results
    expected = {}
    actual = await mock_hub.idemenv.ops.remote_version_list()
    assert expected == actual
