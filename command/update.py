from integration import brew, brew_cask
from pkrglist import parsePkgList
import utils

managers = {"brew": brew.Brew,
            "cask": brew_cask.BrewCask}

def command(args, cfg):
    manager_order = cfg['managers']['order'].splitlines()
    manager_order = [s for s in manager_order if s]

    pkg_path = utils.concatPaths(cfg['paths']['base_path'],
                                 cfg['paths']['pkg_path'])

    for integration in manager_order:

        manager = managers[integration]()

        # Get a list of packages
        pkgs = set()
        for c in manager.getConfigs(pkg_path):
            pkgs = pkgs.union(set(parsePkgList(c)))

        # Update the manager
        print("[" + manager.config_name + "] update")
        if not(args.dry_run):
            manager.update()
        else:
            print(manager.config_name + " would have been updated")

        # Install new packages
        print("[" + manager.config_name + "] install new packages")
        new_pkgs = pkgs.difference(manager.list())
        if not(args.dry_run):
            manager.install(list(new_pkgs))
        else:
            print("The following " + manager.config_name + " would have been installed")
            print(list(new_pkgs))

        # Uninstall old packages
        print("[" + manager.config_name + "] uninstall old packages")
        old_pkgs = manager.list().difference(pkgs)
        if not(args.dry_run):
            manager.uninstall(list(old_pkgs))
        else:
            print("The following " + manager.config_name + " would have been uninstalled")
            print(list(old_pkgs))

        # Update installed packages
        print("[" + manager.config_name + "] update packages")
        if not(args.dry_run):
            manager.upgrade(list(pkgs))
        else:
            print("The following " + manager.config_name + " would have been upgraded")
            print("TODO")