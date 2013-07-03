Intro
=====
This project is a simple fabric script. It makes usual github workflow easy.


Installation
============
1. pip install -r requirements.txt
2. cp local_settings.py.example local_settings.py
3. Configure your local_settings.py
4. Update work shell configuration with alias (add it to ~/.basrc or ~/.zshrc):
    - alias flow="python PATH_TO_FILE/flow.py"


Usage
=====

* `flow change:2000` or `flow change 2000` - creates new branch with name "task-2000" and ask about reseting to last changes from upstream.
* `flow ci -m "Message"` or `flow commit -m "Mesasge"` creates commit with message "Task-2000, Message".
* `flow push` - push commit to origin remote, task-2000 branch.
* `flow pr` - creates pull-request.
* `flow finish -m "Message"` - makes commit, push to branch and create pull-request.
* `flow reset` - take last changes from upstream and applies it to current branch.

We can do all this staff more automatically.
Contributions are welcome!
