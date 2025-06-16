# About this directory.

Load *.py files by application and use as command entry.
Python script must be defined variable which provids entry information.

```python
XXX_COMMAND: Final[dict[str, Any]] = {
    "name": "xxx",
    "procedure": procedure,
    "description": "Explane command."
}
```

An entry information needs 2 or 3 member.
_"name"_ indicates comand token.
After split input string, application search cmmand entry to match 1st token
 and name.
_"description"_ as explane text of command.
It is used by help command. If it is empty string or not defined, command entry
 is not displayed by help command.
_"procedure"_ is a function to execute command.
