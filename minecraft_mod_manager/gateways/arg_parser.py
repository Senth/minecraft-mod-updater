import argparse
import re
from os import path
from typing import Any, List

from ..core.entities.actions import Actions
from ..core.entities.mod import ModArg
from ..core.entities.repo_types import RepoTypes
from ..utils.logger import Logger


def parse_args():
    parser = argparse.ArgumentParser(description="Install or update Minecraft mods from Curseforge")

    parser.add_argument(
        "action",
        choices=Actions.get_all_names_as_list(),
        help="What the application should do.",
    )
    parser.add_argument(
        "mods",
        nargs="*",
        help="The mods to install, update, or configure. "
        + "If no mods are specified during an update, all mods will be updated. "
        + "\nTo specify the download site for the mod you can put 'site:' before the mod. "
        + "E.g. 'curse:litematica'. By default it searches all sites for the mod.\n"
        + "To configure an alias for the mod, use 'mod_name=ALIAS_NAME'. E.g. 'dynmap=dynmapforge'",
    )
    parser.add_argument(
        "-d",
        "--dir",
        type=_is_dir,
        help="Location of the mods folder. By default it's the current directory",
    )
    parser.add_argument(
        "-v",
        "--minecraft-version",
        help="Only update mods to this Minecraft version",
    )
    parser.add_argument(
        "--beta",
        action="store_true",
        help="Allow beta releases of mods",
    )
    parser.add_argument(
        "--alpha",
        action="store_true",
        help="Allow alpha and beta releases of mods",
    )
    parser.add_argument(
        "--mod-loader",
        action="store_true",
        help="Only install forge mods. Rarely necessary to be this explicit",
    )
    parser.add_argument(
        "--mod-loader",
        choices=["fabric", "forge"],
        help="Only install the specified mod of the specified mod loader. "
        + "You rarely need to be this specific. "
        + "The application figures out for itself which type you'll likely want to install.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more messages",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Turn on debug messages. This automatically turns on --verbose as well",
    )
    parser.add_argument(
        "--pretend",
        action="store_true",
        help="Only pretend to install/update/configure. Does not change anything",
    )

    args = parser.parse_args()
    args.action = Actions.from_name(args.action)
    args.mods = _parse_mods(args)
    return args


def _parse_mods(args_mod: Any) -> List[ModArg]:
    mods: List[ModArg] = []
    for mod_arg in args_mod:
        match = re.match(r"(?:(.+):)?([\w-]+)(?:=(.+))?", mod_arg)

        if not match:
            Logger.error(f"Invalid mod syntax: {mod_arg}", exit=True)

        repo_type_name, mod_id, repo_alias = match.groups()
        if repo_type_name and len(repo_type_name) > 0:
            try:
                repo_type = RepoTypes[repo_type_name.lower()]
            except KeyError:
                Logger.error(f"No site named {repo_type_name}")
                Logger.error("Valid names are:")
                for enum in RepoTypes:
                    Logger.error(f"{enum.value}")
                exit(1)
        else:
            repo_type = RepoTypes.unknown

        if not repo_alias:
            repo_alias = mod_id

        mods.append(ModArg(repo_type, mod_id, repo_alias))
    return mods


def _is_dir(dir: str) -> str:
    if path.isdir(dir):
        return dir
    else:
        raise NotADirectoryError(dir)
