# Ovewview

This project is test code to load python module dynamically.

# Execute environment

Python 3.9

# Used development tools

* Visual Studio Code

Extentions: Python, Python debugger, Flake8, Pylance, MyPy Type Checker, Pylint 

# Notes

Confirmed behavior.
* Program could be stopped with specified break point on dynamic loaded script
of VSCode.
* The script file imported by dynamic loaded script are not reload automatically
 'reload' action. It indicats referenced object is not updated by reload.

