# Git and GitHub

## Introduction

- [Git](https://git-scm.com/) is a distributed versioning system.
- **Versioning system** means that git tracks versions of your code (or any other files).
    - It can create snapshots of your code (called **commits**), so you can go back and forth
      between them if needed.
    - You can also work on multiple versions of your code (called **branches**) in parallel.
- **Distributed system** means that the git repository (folder with files tracked by git) can
  be located at multiple places (computers). Git allows you to synchronize changes between these locations easily.
    - One of the locations is usually a cloud repository, accessible via the internet. You can host your git
      repositories
      on services like [GitHub](https://github.com/), [GitLab](https://about.gitlab.com/)
      or [Bitbucket](https://bitbucket.org/).
    - Git becomes indispensable when you collaborate on larger projects with other people. It allows all team members
      to share the same codebase, work on their versions (branches), and merge the changes done by different
      people.

## Creating a GitHub Account

If you do not already have a GitHub account, you can create one here: https://github.com/signup

- Enter your details (username, email, password).
- Verify your email and complete the setup.

### Access token

Later on, when you try to modify your GitHub repository e.g. by ```git push``` command,
you will be asked for your credentials. If you fill in your username and password, you will encounter
the following error:

```
remote: Support for password authentication was removed on August 13, 2021.
remote: Please see https://docs.github.com/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls for information on currently recommended modes of authentication.
fatal: Authentication failed...
```

The simplest way to log in is to get your personal access token (which will de-facto work as a password).
On GitHub page, go to *your account* → *Settings* → *Developer Settings* →
*Personal access tokens* → *Tokens (classic)*.

There, you can generate a new classic token. If you set the token to never expiry and
allow it to perform every action, it will behave as a password.

You can store your credentials on your computer, so you will not be asked for them again:

```commandline
git config credential.helper store
```

This saves your credentials in plaintext in *~/.git-credentials*.
For more secure approaches, you can
use [ssh authentication](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

## Creating a Repository

- Log into your GitHub account.
- Click on the "+" in the top right corner and select *New repository*.
- Fill in the name and other options in the dialog. You can also create an initial README.md file.

You can then clone this repository to your local computer. Click on the *code* button and save the
repository link to the clipboard (or the link in the *Quick setup* section for empty repository). On your computer,
execute

```
git clone link-that-you-just-copied
```

This will create a folder with your repository at your current location. Navigate into that folder.
(Following git commands need to be executed within that folder, otherwise, you will get an error  *fatal: not a git
repository*.)

### Adding files to the repository

Git will track only files that you explicitly add to the git repository by the command

```commandline
git add file_name
```

You can also add multiple files at once, e.g. all R scripts by ```git add *.R``` or all files in the folder
by ```git add .```.

If you prefer adding all files at once, you may find it useful to set up ```.gitignore``` file,
where you specify files that are not added by default -
e.g. you may want to ignore all *.rds* files
(see a [tutorial](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files) for setting-up
*.gitignore*).

After you added some files, you may want to check the status of the repository by

```commandline
git status
```

The command will print some basic info about your git repository; you should see the files you added as *Changes to be
committed*.

Now, you may create your first commit - a snapshot of the repository, with the files that you just added.
To do that, run

```commandline
git commit
```

This will open a command line text editor, where you need to write a commit message
(a description of the changes that you made). You can also specify the commit message
by using the argument ```-m```, e.g.``` git commit -m "Some informative description"```.

You may encounter two caveats at this step:

- If you didn't set up config with your username before, git will ask you for your username. To avoid typing username
  every time you commit
  some changes to git, you may set it up (globally on your computer) by

```
git config --global user.name "your_username"
git config --global user.email "your_email@example.com"
```

- You may not be familiar with the text editor that automatically opens after the ``git commit``
  command. Depending on your setup, the text editor may be
  usually [Vim](https://en.wikipedia.org/wiki/Vim_(text_editor)) or [Nano](https://en.wikipedia.org/wiki/GNU_nano).
  (I strongly suggest using Nano rather than Vim as your default editor, unless you know what you are doing. The Vim is
  not a
  particularly beginner-friendly editor.)
  If you need to close these editors:
    - Vim: Press ESC, then type :wq (write & quit) and press Enter.
    - Nano: Press CTRL + X, then Y to save, and Enter to confirm.

After you successfully commit your changes, it's time to propagate these changes also to the remote repository on
GitHub.
To do that, run

```
git push
```

Git may ask you for your credentials, in which case refer to the section *Access token* above.

If everything went well, you should now see your newly committed files in your repository on GitHub!

## Basic Workflow

The basic workflow of using git may consist of modifying, adding, or deleting files from the repository,
and synchronizing these changes between multiple locations (e.g. your workstation, the GitHub cloud repository, and your
laptop).

- As discussed above, files are not tracked by git until you add them for the first time by the ```git add``` command.
- Creating a git commit (a snapshot of the current version of your code) is actually a two-stage process:
    - At first, you need
      to run ```git add```for the files that you want to commit. This applies also to the files that you already added
      for the first time, but you
      made some changes in them, and you want to commit these changes.
    - After using ```git add``` on new and/or modified files, you create the commit by ```git commit```.
    - This separation between *adding* and *committing* changes allows extra flexibility (you can make a large change to
      your code, but then create multiple commits, each capturing some meaningful block of changes). However, to save
      you
      a bit of time, you may use the ```-a``` argument in ```git commit -a```, which will automatically add changes in
      all
      files
      that are already tracked by git.
- To delete a file, you may use ```git rm file-name```. If you would just delete the file on your computer, you would
  need to also use ```git add```
  or ```git commit -a ```, otherwise, the deletion of the file will not be committed to the git (the same way that
  modifying
  a file
  is not recorded until you run ```git add file-name```). The ```git rm file-name``` command will both delete the file
  on your
  filesystem and also remove the file from git.
- You may stop tracking a previously added file by ```git rm --cached file-name```.
  This way, the file will not be deleted from your computer.
- The difference between the current version of your code and the last commit may be displayed by the
  ```git diff``` command.
- Running ```git push``` command will propagate your local changes to the remote repository on the cloud. You can clone
  the
  repository to multiple places (e.g. if you want to home-office on your laptop)
  by running the ```git clone link-to-repository``` for each of them.
- To synchronize your local repository with the one on GitHub, run ```git pull``` command.
    - You may also use ```git fetch``` to pull the information about changes made in the remote repository, without
      applying them to your local repository.