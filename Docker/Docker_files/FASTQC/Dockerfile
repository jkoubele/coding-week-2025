FROM ubuntu
RUN apt update && apt install curl unzip default-jre perl -y
RUN curl -L -O https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
RUN unzip fastqc_v0.12.1.zip
RUN rm fastqc_v0.12.1.zip
ENV PATH="/FastQC:$PATH"
