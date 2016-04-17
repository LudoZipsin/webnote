#! /usr/bin/env python3

from yapsy.PluginManager import PluginManager
from sh import wkhtmltopdf

import argparse
import urllib
import os
import json
import sys

git_url = "https://github.com/LudoZipsin/my-script"
settings_path = "~/.config/webtonote/settings.json"


def generate_pdf_in(url, destination):
    # expanduser pour destination
    pass


def generate_md_in(url, destination):
    # expanduser pour destination
    pass


def update_backup_location(destination):
    update_json("backup", destination)


def update_default_destination(destination):
    update_json("destination", destination)


def update_json(field, value):
    if not os.path.isdir(os.path.expanduser(value)):
        sys.stderr(value + " is not a valid directory path.\nABORTING")

    with open(os.path.expanduser(settings_path), "r") as json_file:
        conf = json.load(json_file)

    conf[field] = value
    with open(os.path.expanduser(settings_path), "w+") as json_file:
        json_file.write(json.dumps(conf, indent=4, sort_keys=True))


def load_settings():
    with open(os.path.expanduser(settings_path), "r") as json_file:
        conf = json.load(json_file)
    return conf


def get_plugin_path():
    conf = load_settings()
    return conf["plugins"]


def get_backup_path():
    conf = load_settings()
    return conf["backup"]


def get_destination_path():
    conf = load_settings()
    return conf["destination"]


def get_plugin_objet_by_url(url, pl_manager):
    # parse url.base_name
    url_parsed = urllib.parse.urlparse(url)
    plugin_list = [plugin for plugin in pl_manager.getAllPlugins()
                   if url_parsed.netloc
                   in plugin.plugin_object.get_compatible_source()]
    if len(plugin_list) != 1:
        sys.stderr(("ERROR: too many plugin can be used for this url."
                    " can't selected the one to use.\nABORTING"))
    if len(plugin_list) == 0:
        return None
    return plugin_list[0].plugin_object


# def ask_for_location(message):
#    location = input(message)


if __name__ == "__main__":

    ###########################################################################
    #
    #               CONST
    #

    # trois settings important dans le settings path:
    #       - le répertoire par défaut pour les backups
    #       - le répertoire par défaut pour les plugins
    #       - l'emplacement par défaut pour la destination (initiallement, dans
    #         current (.))
    plugins_directory = "~/.config/webtonote/plugins"

    ###########################################################################
    #
    #               PARSER PROCESSING
    #

    arg_parser = argparse.ArgumentParser(description=("Transform web url into"
                                                      " pdf or md reference"))

    # arguments definition ####################################################
    arg_parser.add_argument("url",
                            help=("The url of the web site you want to keep a"
                                  " reference of. Some web site may have"
                                  " special cutsom rules to generate markdown"
                                  " files."
                                  " For more reference, visit: ") + git_url)

    # la première fois que bakcup-pdf sera appelé, on verifie si l'emplacement
    # de sauvegarde est faite. Sinon, propose de le créé (ou de le spécifié).
    arg_parser.add_argument("--backup-pdf",
                            help=("Store a pdf of the web site into a backup"
                                  " folder specified in ") + settings_path + (
                                  " ~/.config/webtonote/settings.json. If no"
                                  " settings exist, it will ask you to"
                                  " register a folder for backup storage."),
                            action="store_true")
    arg_parser.add_argument("--dest",
                            help=("The place you want the referecne file"
                                  " to be generated. If not specified, it"
                                  " will be the location specified in the"
                                  " settings"))
    arg_parser.add_argument("--backup-pdf-only",
                            help=("Generate only a pdf in the backup folder"
                                  " specified in ") + settings_path + (
                                  "If no settings exist, as for --backup-pdf,"
                                  " it will ask you to register a folder for"
                                  " backup storage. THIS OPTION CAN'T BE USED"
                                  " WITH OTHER OPTION EXEPT NAME AND"
                                  " BASE_NAME"),
                            action="store_true")
    arg_parser.add_argument("--md",
                            help=("Change the default format from pdf to"
                                  " markdown. The generated file in the"
                                  " backup folder will remain pdf"),
                            action="store_true")
    # arg_parser.add_argument("--base_name",
    #                        help="Base name of the file")
    arg_parser.add_argument("--name",
                            help=("Name of the file."))# " It can't be used with"
                                  # " base_name option"))

    # end parsing #############################################################
    args = arg_parser.parse_args()

    # start error handling ####################################################

    # no name specified: it will use the one describe in plugin or the url
    # base name with the

    if args.backup_pdf_only is True:
        if args.dest is not None:
            sys.stderr("the option backupt-pdf-only can't be used with --dest")
        if args.backup_pdf is True:
            sys.stderr(("The option backup-pdf-only can't be used with"
                        " --backup-pdf. ABORTING"))
        if args.md is True:
            sys.stderr(("The option backup-pdf-only can't be used with"
                        " --md. ABORTING"))

    ###########################################################################
    #
    #               PLUGIN MANAGEMENT
    #

    plugin_manager = PluginManager()
    plugin_manager.setPluginPlaces([os.path.expanduser(get_plugin_path)])
    plugin_manager.collectPlugins()

    name = args.name
    if name is None:
        plugin = get_plugin_objet_by_url(args.url, plugin_manager)
        if plugin is not None:
            name = plugin.process_name(args.url)
        else:
            name = args.url

    if args.backup_pdf_only is True or args.backup_pdf is True:
        if get_backup_path() == "none":
            # on demande de spécifier un emplacement
            location = input(("Please enter select a directory to use for"
                              " backup. If the location doesn't exist, it will"
                              " be created"))
            update_backup_location(location)
        backup_path = get_backup_path()
        backup_path_full = os.path.expanduser(backup_path)
        wkhtmltopdf(args.url, os.path.join(backup_path_full, name)+".pdf")
    else:
        dest = args.dest
        if dest is None:
            dest = get_destination_path()
            if dest == "current":
                dest = os.path.realpath(os.path.curdir)
            else:
                dest = os.path.expanduser(dest)
        else:
            if dest == ".":
                dest = os.path.realpath(os.path.curdir)
            else:
                dest = os.path.expanduser(dest)

        if args.md is True:
            plugin = get_plugin_objet_by_url(args.url, plugin_manager)
            if plugin is None:
                print(("No plugin to manage this url found. It will generate a"
                       " pdf file instead"))
                wkhtmltopdf(args.url, os.path.join(dest, name)+".pdf")
            else:
                plugin.process_to_md(args.url, os.path.join(dest, name)+".md")
        else:
            wkhtmltopdf(args.url, os.path.join(dest, name)+".pdf")
