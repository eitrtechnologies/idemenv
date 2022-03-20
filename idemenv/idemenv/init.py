def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # The run.py is where your app should usually start
    for dyne in []:
        hub.pop.sub.add(dyne_name=dyne)


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
    print("idemenv works!")
