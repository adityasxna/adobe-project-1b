# download_model.py (run this file once locally, not in Docker)
from sentence_transformers import SentenceTransformer

# This will download the model from the internet and save it to the specified path
model_name = 'all-MiniLM-L6-v2'
model_path = './models/all-MiniLM-L6-v2' # Save it in a new 'models' directory

print(f"Downloading model: {model_name}...")
model = SentenceTransformer(model_name)
model.save(model_path)
print(f"Model saved to {model_path}")
