from pathlib import Path
from textwrap import dedent

import aiofiles

__func_alias__ = {"list_": "list"}


async def list_(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.idemenv.ops.fill_local_version_list()
    current_version = await hub.idemenv.ops.get_current_version()
    version_list = []
    for ver in sorted(hub.idemenv.ops.LOCAL_VERSIONS.keys(), reverse=True):
        prefix = "  "
        suffix = ""
        if ver == current_version[0]:
            prefix = "* "
            suffix = f" (set by {current_version[1]})"
        version_list.append(prefix + ver + suffix)
    print("\n".join(version_list))


async def list_remote(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.idemenv.ops.fill_remote_version_list()
    version_list = sorted(hub.idemenv.ops.REMOTE_VERSIONS.keys(), reverse=True)
    if "latest" in version_list:
        version_list.pop(version_list.index("latest"))
    print("\n".join(version_list))


async def install(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.idemenv.ops.fill_remote_version_list()
    await hub.idemenv.ops.fill_local_version_list()

    if hub.OPT.idemenv.idem_version in hub.idemenv.ops.LOCAL_VERSIONS:
        print(f"{hub.OPT.idemenv.idem_version} is already installed.")
    elif hub.OPT.idemenv.idem_version in hub.idemenv.ops.REMOTE_VERSIONS:
        await hub.idemenv.ops.download_version(hub.OPT.idemenv.idem_version)
    else:
        print(f"ERROR: {hub.OPT.idemenv.idem_version} is not available as a binary.")


async def uninstall(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.idemenv.ops.fill_remote_version_list()
    await hub.idemenv.ops.fill_local_version_list()

    if hub.OPT.idemenv.idem_version in hub.idemenv.ops.LOCAL_VERSIONS:
        await hub.idemenv.ops.remove_version(hub.OPT.idemenv.idem_version)
    else:
        print(f"{hub.OPT.idemenv.idem_version} is already uninstalled.")


async def use(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.idemenv.ops.use_version(hub.OPT.idemenv.idem_version)


async def pin(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    await hub.idemenv.ops.pin_current_version()


async def version(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    current_version = await hub.idemenv.ops.get_current_version()
    if current_version[0]:
        print(f"{current_version[0]} (set by {current_version[1]})")
    else:
        print("ERROR: No version of Idem is set!")


async def init(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    idem_bin = Path(hub.OPT.idemenv.idemenv_dir) / "bin" / "idem"
    idem_bin.parent.mkdir(parents=True, exist_ok=True)

    wrapper = dedent(
        f"""
        #!/usr/bin/env python3

        import os
        import subprocess
        import sys
        from pathlib import Path

        if __name__ == "__main__":
            idemenv_dir = Path("{hub.OPT.idemenv.idemenv_dir}")
            override_version_file = Path(os.getcwd()) / ".idem-version"
            main_version_file = idemenv_dir / "version"

            current_version = ""

            if override_version_file.exists():
                with open(override_version_file, "r") as cfile:
                    current_version = cfile.read()
                    current_version = current_version.replace("\\n", "").strip()

            if not current_version and main_version_file.exists():
                with open(main_version_file, "r") as vfile:
                    current_version = vfile.read()
                    current_version = current_version.replace("\\n", "").strip()

            current_bin = idemenv_dir / "versions" / ("idem-" + current_version)

            if current_version and current_bin.exists():
                del sys.argv[0]
                cmd = (
                    [
                        str(current_bin),
                    ]
                    + sys.argv
                )
                subprocess.call(cmd)
            elif current_version:
                print("ERROR: Version " + current_version + " of Idem is not installed!")
            else:
                print("ERROR: No version of Idem specified!")
        """
    )
    wrapper = wrapper[1:]

    async with aiofiles.open(idem_bin, "w") as ofile:
        await ofile.write(wrapper)
    idem_bin.chmod(0o755)

    print(
        "Add the idemenv bin directory to your PATH:\n\n"
        f"    echo 'export PATH=\"{idem_bin.parent}:$PATH\"' >> ~/.bashrc\n"
        "OR:\n"
        f"    echo 'export PATH=\"{idem_bin.parent}:$PATH\"' >> ~/.zshrc\n"
    )
