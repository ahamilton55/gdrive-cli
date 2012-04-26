#!/bin/sh
find . -name \*.pid -or -name \*.pyc -or -name \*.swp -exec rm -i {} \;
rm -i ${HOME}/.gdrivefs.db

