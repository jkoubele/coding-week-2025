# Cluster usage

## Introduction
We have available a cluster for running computationally demanding jobs.
Respectively, we have 2 clusters available: *old* cluster and the *new* one. 
The *new* cluster is in a process of being set-up. Up to this date (20.2.2025), 
the *new* cluster is not ready yet. The overall logic of the
usage of the *new* cluster should be fairly similar to the *old* one, but
some details may vary. This tutorial refers to the *old* cluster.

To access the cluster, you need to be on our internal network.
Being on the VPN on a laptop is **not** sufficient - in this case, you still
need to *ssh* to your workstation at first (since workstations are located 
on the internal network). 
Accessing the managing server from the workstation can be then done by

```commandline
ssh nmgmt
```

The cluster uses [Slurm](https://slurm.schedmd.com/) system to handle the submission of computational jobs by the users.
You can list a basic overview of the  available computational nodes by the command
```commandline
sinfo
```
The *nmgmt* server is intended only for the management of the jobs via Slurm - no computation should be 
done on the management server directly. 

Both *nmgmt* server and computational nodes have mounted folders from our filesystem.
However, the paths differ from the ones on workstations:

- `/cellfile/data/public` is mounted as `/data/public` on the cluster
- `/cellfile/cellnet` is mounted as `/cellnet` on the cluster

When using the cluster, you need to change all paths used in your scripts accordingly.

Unfortunately, *ssh* to the computational nodes is not allowed.
## Running Jobs
There are 2 ways how to run a job on the computational nodes: interactively via the ```srun``` command,
or non-interactively via the ```sbatch``` command. The interactive job via ```srun``` can be useful for testing and debugging.
The ```sbatch``` method is useful for submitting large amount of jobs.

The ```srun``` command can be used to invoke the terminal, 
thus effectively emulating *ssh*. For example:
```commandline
srun --pty --nodelist=beyer-n02 /bin/bash
```
 - The argument ```--pty``` invokes interactive terminal. Without this option, `srun` would
still displays the output interactively, but the commands submitted to the terminal may not work properly.
 - The ```--nodelist=beyer-n02``` in an optional argument explicitely stating the node on which we want to run the job.
 - For more informaytion about the `srun` command and its arguments, please see [documentation](https://slurm.schedmd.com/srun.html).

After running the `srun` command, you will be located on a node (*beyer-n02*) of the computational cluster.
The data on `/data/public` and `/cellnet` are accessible from there, and you may thus process them
by running scripts/application on the node. However, there are several caveats:
- The cluster nodes are not connected to the internet. This makes it difficult to install or update
any new tools/packages. A possible workaround is to use your workstation to download the necessary files, put them 
on the ```/cellfile/datapublic``` (which is visible as ```/data/public``` on the nodes) and use them to install the desired tools.
For example, R packages may be downloaded as *.tar.gz* files.
- We don't have administrative rights on the cluster.
- Tools already installed on the cluster may be fairly outdated (for example, the R is a version 3.5 from 2018).

A possible strategy is to locate executable binaries of the tools you want to use 
on the shared filesystem and run them from the cluster. For example, running [FASTQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
binaries located on the shared filesystem seems to work, as well as using Python interpreter installed in Anaconda environment.

However, the executable binary files may need additional libraries to be installed on the cluster,
which is generally difficult to accomplish.

### Using Docker on the Cluster

Because of the issues described above, a suitable strategy is to use Docker to run the code/applications you need.
To do that:
1. Use the workstation to obtain a Docker image with the software you need.
2. Save the Docker image as a *.tar* file somewhere on the shared filesystem:
```commandline
docker save -o /path-on-shared-filesystem.tar image-name
```

3. Use ```srun --pty ...``` command to invoke terminal on a node of the cluster.
4. Load the Docker image on the cluster node via  
```commandline
docker load -i docker-image-path.tar
```
5. The image should be now available on the cluster node; you can verify it by ```docker image ls```.
You can use the Docker image to run Docker containers to process your data.



