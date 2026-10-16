import kagglehub

# Download latest version
path = kagglehub.dataset_download("iammustafatz/diabetes-prediction-dataset", output_dir="../data")
print("Path to dataset files:", path)
