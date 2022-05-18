import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import aiofiles
from bs4 import BeautifulSoup

LOCAL_VERSIONS = {}
REMOTE_VERSIONS = {}


async def local_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = {}
    versions_dir = Path(hub.OPT.idemenv.idemenv_dir) / "versions"
    if versions_dir.exists():
        ret = versions_dir.glob("idem-*")
        ret = {ver.name.replace("idem-", ""): ver for ver in ret}
    return ret


async def fill_local_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    hub.idemenv.ops.LOCAL_VERSIONS = await hub.idemenv.ops.local_version_list()


async def remote_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = {}
    ctx = SimpleNamespace(acct={})
    repo_list = await hub.exec.request.raw.get(
        ctx,
        url=hub.OPT.idemenv.repo_url,
    )
    if repo_list.get("ret"):
        soup = BeautifulSoup(repo_list["ret"], "html.parser")
        ret = {
            re.sub(r"-\d+$", "", node["href"][:-1]): node["href"][:-1]
            for node in soup.find_all("a")
            if node.get("href") and node["href"].endswith("/") and node["href"] != "../"
        }
    return ret


async def fill_remote_version_list(hub, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    hub.idemenv.ops.REMOTE_VERSIONS = await hub.idemenv.ops.remote_version_list()


async def download_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    ret = False
    ctx = SimpleNamespace(acct={})
    if not hub.idemenv.ops.REMOTE_VERSIONS:
        await hub.idemenv.ops.fill_remote_version_list()

    if version in hub.idemenv.ops.REMOTE_VERSIONS:
        url = hub.OPT.idemenv.repo_url
        if not url.endswith("/"):
            url += "/"
        url += hub.idemenv.ops.REMOTE_VERSIONS[version]
        file_list = await hub.exec.request.raw.get(
            ctx,
            url=url,
        )
        soup = BeautifulSoup(file_list["ret"], "html.parser")
        links = [
            node["href"]
            for node in soup.find_all("a")
            if node.get("href") and not node["href"].endswith("/") and node["href"] != "../"
        ]

        pkg_name = ""
        # TODO: verify download with SHA/GPG
        for link in links:
            if sys.platform in link:
                pkg_name = link

        if pkg_name:
            outfile = Path(hub.OPT.idemenv.idemenv_dir) / "downloads" / pkg_name
            outfile.parent.mkdir(parents=True, exist_ok=True)
            versions_dir = Path(hub.OPT.idemenv.idemenv_dir) / "versions"
            versions_dir.mkdir(parents=True, exist_ok=True)
            idem_bin_out = versions_dir / f"idem-{version}"

            download_url = "/".join(
                [
                    url,
                    pkg_name,
                ]
            )

            pkg = {}
            if not outfile.exists():
                pkg = await hub.exec.request.raw.get(
                    ctx,
                    url=download_url,
                )
                async with aiofiles.open(outfile, "wb") as ofile:
                    await ofile.write(pkg["ret"])

            if (outfile.exists() and not idem_bin_out.exists()) or (pkg and pkg["status"] == 200):
                print("Processing download...")
                outfile.rename(idem_bin_out)
                idem_bin_out.chmod(0o755)
                ret = idem_bin_out.exists()
    return ret


async def get_current_version(hub, **kwargs):
    """
    Read the current active version from ./.idem-version and the main version
    file at ${SALTENV_DIR}/version. The former overrides the latter.
    """
    ret = ("", "")
    override_version_file = Path(os.getcwd()) / ".idem-version"
    main_version_file = Path(hub.OPT.idemenv.idemenv_dir) / "version"

    if override_version_file.exists():
        async with aiofiles.open(override_version_file, "r") as cfile:
            current_version = await cfile.read()
            current_version = current_version.replace("\n", "").strip()
        ret = (current_version, str(override_version_file))

    if not ret[0] and main_version_file.exists():
        async with aiofiles.open(main_version_file, "r") as vfile:
            current_version = await vfile.read()
            current_version = current_version.replace("\n", "").strip()
        ret = (current_version, str(main_version_file))

    return ret


async def pin_current_version(hub, **kwargs):
    """
    Get the current active version and write it to ./.idem-version
    """
    ret = False
    current_version = await hub.idemenv.ops.get_current_version()
    override_version_file = Path(os.getcwd()) / ".idem-version"

    if current_version[0]:
        async with aiofiles.open(override_version_file, "w") as ofile:
            await ofile.write(current_version[0])
        ret = True

    return ret


async def remove_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    idem_bin = hub.idemenv.ops.LOCAL_VERSIONS.get(version)
    if idem_bin:
        idem_bin.unlink()

    return True


async def use_version(hub, version, **kwargs):
    """
    This is the entrypoint for the async code in your project
    """
    if not hub.idemenv.ops.LOCAL_VERSIONS:
        await hub.idemenv.ops.fill_local_version_list()

    if version in hub.idemenv.ops.LOCAL_VERSIONS:
        version_file = Path(hub.OPT.idemenv.idemenv_dir) / "version"
        version_file.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(version_file, "w") as vfile:
            await vfile.write(version)
    else:
        print(f"{version} is not installed. Run 'idemenv install {version}' first.")

    return True
