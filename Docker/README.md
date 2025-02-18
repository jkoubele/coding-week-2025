# Docker

## Introduction

- [Docker](https://www.docker.com/) is a tool for virtualization on the level of an operating system.
    - It's similar to a virtual machine (VM). However, Docker is fast, with practically no overhead.
- Docker **container** is an isolated environment, in which you can run your code/applications.
  It emulates an operating system (so you can run e.g. Ubuntu container on a Windows computer).
- A template for containers is called Docker **image**. It specifies the operating system and installed tools/packages.
  You can download ready-made docker images from [Dockerhub](https://hub.docker.com/),
  or create your own (by extending some pre-existing image).
- Docker may be useful for the following reasons:
    - It improves the reproducibility of your code. You may create a Docker image
      with specific versions of applications and packages. You may then share the image,
      with the correct version of all packages (and also the operating system) already installed.
    - You may run software that is available only for a specific OS (e.g. if you have a Windows
      computer and want to run a Linux software).
    - Since Docker containers are isolated from the host computer, you have admin privileges inside them, even if you
      are not an admin on the host computer. This allows you to install whatever tools/packages you need, which is
      useful e.g. for running a code on a computational cluster.

## Getting Started

- To run a Docker container, you will need to get some Docker image first. You can list
  all image you have by

```commandline
docker image ls
```

- You may get images from [Dockerhub](https://hub.docker.com/), which is a default remote repository of docker images.
  For example, you may search for [Ubuntu image](https://hub.docker.com/_/ubuntu), and then download it by

```commandline
docker pull ubuntu
```

Docker images also have tags (version). By default, the image with tag ```:latest``` is used, but you may specify
the tag to get some [older version](https://hub.docker.com/_/ubuntu/tags) of the image,
e.g. ```docker pull ubuntu:20.04```.

## Running a Container

You may run a container in either interactive or non-interactive way. To begin with, we will run a container from the
Ubuntu image
in interactive way (by using the ```-it``` argument):

```commandline
docker run -it ubuntu
```

If you don't have the image with given name available, Docker will search for it on DockerHub and try to pull it, if
such image exists (therefore, you don't necessarily need to run ```git pull``` before that).

After running the container, you will start an interactive session inside the container.

You may list all running container by running

```commandline
docker ps
```

on your host machine (not inside the container).

You may exit the running container by typing ```exit``` inside it.

In the container, you are signed as a *root* user, which allow you to e.g. install whatever software you want.
However, so far the container is isolated from your host machine, so you cannot get any output from the container
to your machine easily. Also, any modification (e.g. installing a software) you do inside the container will be lost
after
the container is stopped.

We will now address both of these issue, by installing a software
inside the docker image, so every container run from that image will have the software already available.
Also, we will then mount the docker container to filesystem of the host machine, allowing it to process data on our
computer.

## Creating a Docker Image from a Dockerfile

*Dockerfile* is a template for creating (so-called building) Docker images.
Dockerfile is a text file, by default named *Dockerfile* (without any extension).

Following is an example of a simple Dockerfile:

```dockerfile
FROM ubuntu
RUN apt update && apt install curl unzip default-jre perl -y
RUN curl -L -O https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
RUN unzip fastqc_v0.12.1.zip
RUN rm fastqc_v0.12.1.zip
ENV PATH="/FastQC:$PATH"
```

- The Dockerfile specifies the starting image by the ```FROM``` instruction;
  here, we are starting our build from a plain Ubuntu image.
- The ```RUN```instructions are used to run command line commands during the build. Here,
  we are installing several tools by *apt install*, and then downloading and extracting
  [FASTQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
  (a tool used for quality control of reads in FASTQ files).
- The ```ENV``` instruction is used to set environment variables (here, the location
  of the installed FASTQC tool is added to PATH).
- For additional instruction available in Dockerfile syntax, please see
  the [documentation](https://docs.docker.com/reference/dockerfile/).

The Dockerfile described above is also saved in this repository [here](./Docker_files/FASTQC/Dockerfile).

To build the Docker image, run

```commandline
docker build -t fastqc-example /path-to-folder-with-dockerfile
```

The argument ```-t```specifies the name of the newly built image.
After a successful build, you should see the new image listed after running ```docker image ls```.
If you now run the docker image in the interactive mode by

```commandline
docker run -it fastqc-example
```

the tools installed during the build should be available in the running container.

## Mounting a Folders from Host Filesystem

To make a folder from the host computer accessible in a running Docker container,
you can mount the folder by the ```-v``` argument. Following the example above, we may use the FASTQC tool
we installed to process FASTQ data from RNA-seq.
This repository contain a [folder](./example_data) with an example *.fastq* file.
You can run a container with a mounted folder by

```commandline
docker run -it -v path-to-folder-on-host-computer:/data fastqc-example
```

The folder ```/data``` after the colon ```:``` in the argument ```path-to-folder-on-host-computer:/data```
is an arbitrary name that will be used to name the folder inside the container.

Inside the container, you may then run

```commandline
fastqc /data/reads.fastq
```

This should create an output of the FASTQC tool located in the mounted folder; you can access these files
from your host computer.

It can happen that the newly created files will be read-only or otherwise locked (this is because they were created the
*root* user inside the container). You can fix that by running

```commandline
chmod -R 777 /data
```

from the Docker container.

## Running Containers in a Non-interactive Way

The default command executed by the Docker container is usually to run */bin/bash*. If you run the container
interactively by using the ```-it``` argument, this is the reason why the command line (bash)
will be open. The default command may be specified by the ```CMD``` instruction in the Dockerfile. Some
Docker images may have a different default command - for example, the [r-base image](https://hub.docker.com/_/r-base) has
a default command to run R.

You may run a command in the non-interactive way by omitting the ```-it``` argument in the ```docker run```.
In this case, you should provide the command that should be executed (otherwise, the container will
terminate immediately, as it will open *bash* and find no command to be run there). For example, you may run
```commandline
docker run -v path-to-folder-on-host-computer:/data  fastqc-example fastqc /data/reads.fastq
```
This will make the *fastqc-example* container execute the command ```fastqc``` with the file */data/reads.fastq* as an argument. After that, 
the container will terminate.

It may be useful to also run the container in the detached mode by using the argument ```-d```. In this way,
the container will not block your command line. Using the detached mode, you may create
e.g. a script that runs multiple docker containers at once, each processing some part of your data.