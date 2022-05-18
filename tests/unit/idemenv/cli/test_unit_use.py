from unittest.mock import AsyncMock
from unittest.mock import MagicMock


async def test_unit_use(mock_hub, hub):
    # Link the function to the mock_hub
    mock_hub.idemenv.cli.use = hub.idemenv.cli.use

    mock_hub.idemenv.ops.use_version = AsyncMock()

    mock_hub.OPT.idemenv.idem_version = MagicMock()

    # Call the use function
    await mock_hub.idemenv.cli.use()

    # Confirm that use_version was called with the idem_version value
    mock_hub.idemenv.ops.use_version.assert_called_once_with(mock_hub.OPT.idemenv.idem_version)
