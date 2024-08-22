# Introduction to the Development Environment


This lab is in a Jupyter notebook (`assignment-lab.ipynb`).  To run it'll you'll need to
check out the assignment-lab.

This document describe how to do those two things.  Then, you'll be able to
open the Jupyter notebook and proceed with lab itself.

# Software You Will Need

**Note** Safari and Internet Explorer are not currently supported.  This will
probably be fixed by the next lab, but for this lab you should use Chrome
(first choice, most tested) or Firefox.  Edge Seems to be ok.

Jupyter Notebook is an interactive computing enviroment for gathering and
displaying data (among other things).

The content for each lab will be distributed via github classroom.

So, to do the assignment of this course, you need:
1. You'll need to log into https://escalab.org/datahub to run a jupyter notebook. 
2. Tha asssignment from github classroom.  Find the link on the course 
home page: https://www.escalab.org/classes/cse142-2024su/

## Connecting to cse142 jupyterhub 

The first step is to navigate your browser to 
https://escalab.org/datahub

One of two things will happen:

1. You'll find yourself at a nice home page and you can click the big orange "Log In" button. 

2. If you've used the system before/recently it might drop you directly into a jupyter notebook file browser.

If you it's #2, you will need to click "Control Panel" (upper right) and then
click the big red "Stop My Server" button, if it's there.  If it's not, that's
fine.  Then click "Logout" (upper right) to get back to the homepage and the
big orange button.

Now, click the big orange button and login with your `@ucsd.edu` email address.
After a progress bar, you'll end up at the Jupyter Notebook file browser.
Looking at an empty directory (unless you've used the Datahub before, in which
case your old files will be there).  In any case, you don't have a lab to do
yet.

You can now proceed with the instructions below for cloning the lab repo.  Once
you complete them, you can return to the Jupyter Notebook file browser and open
your lab notebook.

### Important Note

Jupyterhub tries to keep your session alive, so if you navigate away and then come
back later, your notebook will still be there and it will initially seem to be
working, but then commands in the notebook will start failing and complaining
about "stale file handles". If this happens, you need to go to "control panel"
and stop your server and then restart it.

## Cloning the Assignment Repo

First, accept the assignement on Github Classroom.  It's available via the
cse142 [home page](https://www.escalab.org/classes/cse142-2024su/).

This will set you up with a copy of the starter repository.

**Note**: Be sure to use the **`ssh`** method to checkout your repo rather than `http`.  Authentication over ssh is much simpler and it's what our tools assume.  If you try to use HTTP, you'll get something like:

```
[htseng@datahub]$ git clone https://github.com/cse142ucsd/2024su-cse142-welcome-hungweitseng.git
Cloning into '2024su-cse142-welcome-hungweitseng'...
Username for 'https://github.com': hungweitseng
Password for 'https://hungweitseng@github.com': 
remote: Support for password authentication was removed on August 13, 2021.
remote: Please see https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls for information on currently recommended modes of authentication.
fatal: Authentication failed for 'https://github.com/cse142ucsd/2024su-cse142-welcome-hungweitseng.git/'
```
![clone with ssh](images/clone-with-ssh.png)


You'll need to open a terminal from jupyterhub.  From the file browser, lect "new->terminal" from the menu in the upper right.
At the resulting Linux prompt, you can `git clone` the repo locally.

![Log into datahub](images/open-terminal-short.gif)


You may need to create an ssh key and add it to your github account.  You can create the key with (in your jupyterhub terminal):

```
ssh-keygen
```

and accept the defaults.  I recommend no password, so you don't have to type it all the time.

Then view your new public key:

```
cat ~/.ssh/id_rsa.pub
```

Then follow these instructions:

https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account


## Open the Notebook

Switch to the tab with file browser and navigate to the directory you just cloned.   Click on `assignment-lab.ipynb` to open the lab and get to work!

**Note:** You'll need to trust the notebook when Jupyter asks.
