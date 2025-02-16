# Git and GitHub

## Introduction

- [Git](https://git-scm.com/) is a distributed versioning system.
- **Versioning system** means that git tracks versions of your code (or any other files).
    - It can create snapshots of you code (called **commits**), so you can go back and forth
      between them if needed.
    - You can also work on multiple versions of your code (called **branches**) in parallel.
- **Distributed system** means that git repository (folder with files tracked by git) can
  be located at multiple places (computers). Git allows you to easily synchronize changes between these locations.
    - One of the locations is usually a cloud repository, accessible via internet. You can host your git repositories
      on services like [GitHub](https://github.com/), [GitLab](https://about.gitlab.com/)
      or [Bitbucket](https://bitbucket.org/).
    - Git becomes indispensable when you collaborate on larger project with other people. It allows all team members
      to share the same codebase, work on their versions (branches) and merge together the changes done by different
      people.

## Creating a GitHub Account

If you do not already have a GitHub account, you can create one here: https://github.com/signup

- Enter your details (username, email, password).
- Verify your email and complete the setup.

### Access token
Later on, when you will try to modify your GitHub repository e.g. by ```git push``` command,
you will be asked for your credentials. If you fill in your username and password, you will encounter 
the following error:
```
remote: Support for password authentication was removed on August 13, 2021.
remote: Please see https://docs.github.com/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls for information on currently recommended modes of authentication.
fatal: Authentication failed...
```
The simplest way to login is to get your personal access token (which will de-facto work as a password).
On GitHub page, go to *your account* -> *Settings* -> *Developer Settings* ->
Personal access tokens -> *Tokens (classic)*.

There, you can generate new classic token. If you set the token to never expiry and 
allow it to perform every action, it will behave as a password. 

You can store your credentials on your computer, so you will not be asked for them again:
```commandline
git config credential.helper store
```
This saves your credentials in plaintext in *~/.git-credentials*. 
For more secure approaches, you can use [ssh authentication](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).