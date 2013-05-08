Intro
=====
This project is script for fabric. It simplify work with mmp project workflow.


Installation
============
1. pip install -r requirements.txt
2. cp local_settings.py.example local_settings.py
3. Enter your GITHUB credentials into local_settings.py
4. update work shell configuration with alias:
    - alias flow="python PATH_TO_FILE/flow.py"


Usage
=====
- flow change:2000
- flow ci -m "Message"
- flow finish -m "Message"
- flow push -f
- flow reset
