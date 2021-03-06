Intro
=====
This project is a simple fabric script. It makes usual github workflow easy.


Installation
============

```bash
$ python setup.py install
```

or

```bash
$ pip install -e git+https://github.com/vasyabigi/ds-flow#egg=dsflow
```

And make your own config file here: `~/.flow`. Example:

```bash
[global]
GITHUB_USER:username
GITHUB_PASS:secret
UPSTREAM_ONLY:False
GIT_ADD_FIRST:True
GIT_REBASE_FIRST:True
GITHUB_PULL_REQUEST_URL:https://api.github.com/repos/django-stars/repo/pulls
```

Usage
=====

![](https://dl.dropboxusercontent.com/s/3hqckklxnfthq76/flowscreenshot.png)

* `flow change:2000` or `flow change 2000` - creates new branch with name "task-2000" and ask about reseting to last changes from upstream.
* `flow ci -m "Message"` or `flow commit -m "Mesasge"` creates commit with message "Task-2000, Message".
* `flow push` - push commit to origin remote, task-2000 branch.
* `flow pr` - creates pull-request.
* `flow finish -m "Message"` - makes commit, push to branch and create pull-request.
* `flow reset` - take last changes from upstream and applies it to current branch.


Similar projects
================

* [gitflow](https://github.com/nvie/gitflow)
* [legit](http://www.git-legit.org/)


Authors
=======
* Volodymyr Pavlenko [@mindinpanic](https://github.com/mindinpanic)
* Vasyl Stanislavchuk [@vasyabigi](https://github.com/vasyabigi)
* Vasyl Dizhak [@rootart](http://github.com/rootart)

We can do all this staff more automatically.
Contributions are welcome!
