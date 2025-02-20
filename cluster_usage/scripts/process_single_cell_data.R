library(Seurat)
library(argparse)
library(ggplot2)

options(future.globals.maxSize = 4 * 1024^3)  # Increases parallelization limit (used by SCTransform) to 4 GB


parser <- ArgumentParser()
parser$add_argument('--input_folder',
                    default = '/cluster_usage/data/GSE147319/GSM4425801',
                    help = 'Path to input folder')
parser$add_argument('--output_folder',
                    default = '/cluster_usage/output/GSE147319/GSM4425801',
                    help = 'Path to output folder')

args <- parser$parse_args()
input_folder <- args$input_folder
output_folder <- args$output_folder

count_matrix <- ReadSTARsolo(input_folder)

num_pca_dims <- 30
seurat_object <- CreateSeuratObject(count_matrix) |>
  SCTransform() |>
  RunPCA() |>
  FindNeighbors(dims = 1:num_pca_dims, reduction = 'pca') |>
  FindClusters() |>
  RunUMAP(dims = 1:num_pca_dims)


# UMAP plot
umap_by_cluster <- DimPlot(seurat_object, reduction = 'umap', group.by = "seurat_clusters") +
  labs(title = "UMAP by cluster")
ggsave(file.path(output_folder, "umap_cluster.png"),
       plot = umap_by_cluster,
       bg = 'white')

# save metadata to .tsv
write.table(seurat_object@meta.data,
            file = file.path(output_folder, 'seurat_metadata.tsv'),
            sep = '\t',
            quote = FALSE,
            row.names = TRUE)

