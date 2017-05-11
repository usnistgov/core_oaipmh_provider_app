#!/bin/bash
SCRIPT_PATH=`dirname $0`

python -m unittest discover -s ${SCRIPT_PATH}/.. -p "tests_unit*.py"
