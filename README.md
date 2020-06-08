# dep-smell-checker

This command line tool will analyze your Javascript dependencies and notify you of potential dependency smells, listed below.

* Pinned dependency
* Restrictive dependency
* Permissive dependency
* URL dependency
* Missing package-lock
* Unused dependency
* Missing dependency

## Prerequisites

This tool relies on the depcheck tool from npmjs for finding unused and missing dependencies, found here:
https://www.npmjs.com/package/depcheck

## How to Run?

Simply run the tool.py with the project directory as a command-line parameter

e.g.: ```python tool.py /Users/me/Desktop/project```
