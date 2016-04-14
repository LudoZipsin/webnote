#! /usr/bin/env python3

import argparse
import urlparse3
import os

if __name__ == "__main__":

    ###########################################################################
    #
    #               CONST
    #

    git_url = "https://github.com/LudoZipsin/my-script"
    settings_path = "~/.config/webnote/settings.json"
    # trois settings important dans le settings path:
    #       - le répertoire par défaut pour les backups
    #       - le répertoire par défaut pour les plugins
    #       - l'emplacement par défaut pour la destination (initiallement, dans
    #         current (.))
    plugins_directory = "~/.config/webnote/plugins"

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
                                  " ~/.config/webnote/settings.json. If no"
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
    arg_parser.add_argument("--base_name",
                            help="Base name of the file")
    arg_parser.add_argument("--name",
                            help=("Name of the file. It can't be used with"
                                  " base_name option"))

    # end parsing #############################################################
    args = arg_parser.parse_args()

    # start error handling ####################################################
