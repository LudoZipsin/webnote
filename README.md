__work in progress finished. Some issues may still be there. Use with caution__

# Webtonote

This little script is there to help managing reference from the web. Give it an url and some otpions, it will generate the pdf or markdown associated to the url (pdf with wkhhtmltopdf, md with custom plugin)

## Dependencies

This script use the program:

* [wkhtmltopdf](http://wkhtmltopdf.org/)

And the pyhton packages (install it with ```pip3 install```): 

* [sh](https://amoffat.github.io/sh/)
* [yapsy](http://yapsy.sourceforge.net/)
* [argparse](https://docs.python.org/3/library/argparse.html)
* [json](https://docs.python.org/3/library/json.html)

## Plugins

For your most used website, you can make your own plugin with pyhton to scrap the site and generate the md file. 

A plugin may have this three following methods:

* ```process_to_md(url)```
* ```process_name(url)```
* ```get_compatible_source()```

Two file are required for the plugins to work:

* __my.plugin.name.py__ : this file contains the code for your plugin. Most certainly with beautiful soup if you want to scrap html content
* __my.plugin.name.yapsy-plugin__ : this file contains the description for your plugin. Refer to [yapsy](http://yapsy.sourceforge.net/) for more information on how to build a plugin.
