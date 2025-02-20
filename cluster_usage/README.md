# Cluster usage

## Introduction

We have a cluster available to run computationally demanding jobs.
Respectively, we have 2 clusters available: *the old* cluster and the *new* one.
The *new* cluster is in the process of being set up. Up to this date (20.2.2025),
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
You can list a basic overview of the available computational nodes by the command

```commandline
sinfo
```

The *nmgmt* server is intended only for the management of the jobs via Slurm - no computation should be
done on the management server directly.

Both the *nmgmt* server and the computational nodes have mounted folders from our filesystem.
However, the paths differ from the ones on workstations:

- `/cellfile/datapublic` is mounted as `/data/public` on the cluster.
- `/cellfile/cellnet` is mounted as `/cellnet` on the cluster.

When using the cluster, you need to change all paths used in your scripts accordingly.

Unfortunately, *ssh* to the computational nodes is not allowed.

## Running Jobs

There are 2 ways how to run a job on the computational nodes: interactively via the ```srun``` command,
or non-interactively via the ```sbatch``` command. The interactive job via ```srun``` can be useful for testing and
debugging.
The ```sbatch``` method is useful for submitting a large amount of jobs.

The ```srun``` command can be used to invoke the terminal,
thus effectively emulating *ssh*. For example:

```commandline
srun --pty --nodelist=beyer-n02 /bin/bash
```

- The argument ```--pty``` invokes interactive terminal. Without this option, `srun` would
  still display the output interactively, but the commands submitted to the terminal may not work properly.
- The ```--nodelist=beyer-n02``` is an optional argument explicitly stating the node on which we want to run the job.
- For more information about the `srun` command and its arguments, please
  see [documentation](https://slurm.schedmd.com/srun.html).

After running the `srun` command, you will be located on a node (*beyer-n02*) of the computational cluster.
The data on `/data/public` and `/cellnet` are accessible from there, and you may thus process them
by running scripts/applications on the node. However, there are several caveats:

- The cluster nodes are not connected to the internet. This makes it difficult to install or update
  any new tools/packages. A possible workaround is to use your workstation to download the necessary files, put them
  on the ```/cellfile/datapublic``` (which is visible as ```/data/public``` on the nodes), and use them to install the
  desired tools.
  For example, R packages may be downloaded as *.tar.gz* files.
- We don't have administrative rights on the cluster.
- Tools already installed on the cluster may be fairly outdated (for example, the R version is 3.5 from 2018).

A possible strategy is to locate executable binaries of the tools you want to use
on the shared filesystem and run them from the cluster. For example,
running [FASTQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
binaries located on the shared filesystem seem to work, as well as using the Python interpreter installed in Anaconda
environment.

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

3. Use ```srun --pty ...``` command to invoke the terminal on a node of the cluster.
4. Load the Docker image on the cluster node via

```commandline
docker load -i docker-image-path.tar
```

5. The image should be now available on the cluster node; you can verify it by ```docker image ls```.
   You can use the Docker image to run Docker containers to process your data.

### Using Sbatch

The main benefit of the cluster is that it allows us to submit many jobs and run them in parallel, using all computational nodes available. A suitable
approach for that is to use the ```sbatch``` command rather than the ```srun```. The ```sbatch``` command is
not interactive (it will not block your terminal), which is useful for submitting many jobs at once.

### Example: Analysis of Single-Cell Data

We will now provide an example of analyzing scRNA-seq data from the dataset
[GSE147319](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE147319). The dataset
consists of 8 samples (specified by GSM ID). The raw reads were already processed
by the STARsolo aligner, and we have available the output in the form of count matrices.

1. We build an appropriate Docker image and save it to the shared filesystem.
2. We prepare an R script that takes the input and output locations as arguments
   and contains code processing the data.
3. We create a shell script wrapping the R script into a Docker container.
4. The ```sbatch``` job can be submitted e.g. by

```
sbatch single_cell_processing_job.sh -i /data/public/jkoubele/coding-week-2025/cluster_usage/data/GSE147319/GSM4425801 -o /data/public/jkoubele/coding-week-2025/cluster_usage/output/GSE147319/GSM4425801 -s /data/public/jkoubele/coding-week-2025/cluster_usage/scripts -d /data/public/jkoubele/coding-week-2025/cluster_usage/custom_bioconductor.tar
```

5. The job was submitted to the Slurm queue, which we may display be the command

```
squeue
```
6. We may run a loop over all our samples, submitting each to be processed by one *sbatch* job.






