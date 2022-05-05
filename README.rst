.. image:: https://github.com/pedrohavay/transgit/blob/main/docs/transgit.png?raw=true
  :alt: TransGit Logo

TransGit
========

TransGit is a tool created to facilitate the export of repositories from
a GitLab instance to GitHub.

::

   transgit -u <GITLAB-URL> -t <GITLAB-TOKEN> -gu <GITHUB-USER> -p <GITHUB-PERSONAL-TOKEN>

The tool clones all repositories to your machine and then performs the
export process to GitHub using the REST API.

Features
--------

-  Export GitLab repositories to personal or organization Github

-  Export the repositories of specific groups

-  Archive repositories after export

-  Compatibility with Git filter-repo

-  Allows you to change the information of the commits such as, for
   example, the user name, e-mail and among others.

Install
-------

If you have Pip installed on your system, you can use it to install the
latest TransGit stable version:

::

   $ sudo pip3 install transgit

Only versions >=3.5 are supported.

Disclaimer
----------

This software must not be used on third-party servers without
permission. TransGit was created to ease the process of migrating Git
instances.
