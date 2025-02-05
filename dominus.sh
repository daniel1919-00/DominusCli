#!/bin/sh
if command -v python3 > /dev/null 2>&1; then
    PYTHON_CMD=python3
elif command -v python > /dev/null 2>&1; then
    PYTHON_CMD=python
else
    echo "Python is not installed. Exiting."
    exit 1
fi

$PYTHON_CMD -m pip install -q -r ./requirements.txt
if [ $? -ne 0 ]; then
    echo "pip install failed. Exiting."
    exit 1
fi

$PYTHON_CMD ./dominus_cli/run.py