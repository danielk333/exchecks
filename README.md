# exchecks
Python package to track long running executions

## Install

```
pip install git+https://github.com/danielk333/exchecks
```

## Usage

For fish shell the exit code of the last command is stored in `$status`.

```bash
exchecks record &; long-running-command; exchecks exit $status;
```