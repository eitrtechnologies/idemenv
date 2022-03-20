def test_cli(mock_hub, hub):
    mock_hub.idemenv.init.cli = hub.idemenv.init.cli
    mock_hub.idemenv.init.cli()
    mock_hub.pop.config.load.assert_called_once_with(["idemenv"], "idemenv")
