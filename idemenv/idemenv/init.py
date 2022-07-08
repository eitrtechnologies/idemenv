def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # The run.py is where your app should usually start
    for dyne in ["acct", "exec", "tool"]:
        hub.pop.sub.add(dyne_name=dyne)
    for dyne in ["exec", "tool"]:
        hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)


def cli(hub):
    hub.pop.config.load(["idemenv"], cli="idemenv")
    # Your app's options can now be found under hub.OPT.idemenv
    kwargs = dict(hub.OPT.idemenv)

    # Initialize the asyncio event loop
    hub.pop.loop.create()

    # Start the async code
    coroutine = hub.idemenv.init.run(**kwargs)
    hub.pop.Loop.run_until_complete(coroutine)


async def run(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    if hub.SUBPARSER == "init":
        return await hub.idemenv.cli.init()
    elif hub.SUBPARSER == "install":
        return await hub.idemenv.cli.install()
    elif hub.SUBPARSER == "list":
        return await hub.idemenv.cli.list()
    elif hub.SUBPARSER == "list-remote":
        return await hub.idemenv.cli.list_remote()
    elif hub.SUBPARSER == "pin":
        return await hub.idemenv.cli.pin()
    elif hub.SUBPARSER == "uninstall":
        return await hub.idemenv.cli.uninstall()
    elif hub.SUBPARSER == "use":
        return await hub.idemenv.cli.use()
    elif hub.SUBPARSER == "version":
        return await hub.idemenv.cli.version()
    else:
        print(hub.args.parser.help())
        return 2
