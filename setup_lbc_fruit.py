from distutils.core import setup
import py2exe

setup(
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "excludes": ["_ssl", "pywin", "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", "pywin.dialogs.list", "pyreadline", "difflib", "doctest", "optparse", "pickle", "calendar", "pdb", "unittest", "inspect", "Tkconstants", "Tkinter", "tcl"],
                          "dll_excludes": ["msvcp90.dll"],
                          "bundle_files": 1}},
    zipfile = None,
    version = "1.5",
    description = "Fruit basket program using Layout by Code for Python",
    name = "Lbc Fruit",

    windows = ["lbc_fruit.py"],
    )
