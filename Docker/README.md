# Docker

## Introduction

- Docker is a tool for virtualization on a level of operating system.
    - It's similar to a virtual machine (VM). However, Docker is fast, with practically no overhead.
- Docker **container** is an isolated environment, in which you can run your code/applications.
  It emulates an operating system (so you can run e.g. Ubuntu container on a Windows computer).
- A template for containers is called Docker **image**. It specifies the operating system and installed tools/packages.
  You can download ready-made docker images from [Dockerhub](https://hub.docker.com/),
  or create your own (by extending some pre-existing image).
- Using Docker may be useful for the following reasons:
    - It improves the reproducibility of your code. You may create a Docker image
      with specific versions of applications and packages. You may then share the image,
      with to correct version of all packages (and also the operating system) already installed.
    - You may run software that is available only for a specific OS (e.g. if you have a Windows
      computer and want to run a Linux software).
    - Since Docker containers are isolated from the host computer, you have admin privileges inside them, even if you
      are not an admin on the host computer. This allows you to install whatever tools/packages you need, which is
      useful e.g. for running a code on a computational cluster.