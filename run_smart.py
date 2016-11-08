#!/usr/bin/env python

import sys

from smart_house import start_smart

if __name__ == "__main__":
    try:
        sys.exit(start_smart.main())
    except Exception as ex:
        print ex
