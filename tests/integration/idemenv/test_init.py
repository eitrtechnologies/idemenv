from unittest import mock


def test_cli(hub):
    with mock.patch("sys.argv", ["idemenv"]):
        hub.idemenv.init.cli()
