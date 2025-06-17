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

# How to execute.

1. Clone project by git.

2. If need, make venv(virtual environment).

When using python executable.
```
# python3 -m venv venv
```
When using seveal version on windows with py.exe.
```
# py -3.9 -m venv venv
```

Apply virtual environment. Below example is bash.
```
# ./venv/Scripts/activate
```

3. Run application.

```
# python main.py
```

# VSCode launch.json example.

.vscode/lanunch.json
```
{
    "version": "0.2.0",
    "configurations": [
       {
            "name": "Execute application.",
            "type": "debugpy",
            "request": "launch",
            "program": "main.py",
            "console": "integratedTerminal",
            "args": ""
        }
    ]
}
```


