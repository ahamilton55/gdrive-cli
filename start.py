#!/usr/bin/env python

from oauth import simple_cli

credentials = simple_cli.authenticate()
from pprint import pprint
pprint(credentials)

