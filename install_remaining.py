import subprocess
import sys

def install_remaining():
    packages = [
        "transformers>=4.20.0",
        "tokenizers>=0.13.0", 
        "xgboost>=1.6.0",
        "mlflow>=1.30.0",
        "python-dotenv>=0.19.0",
        "tqdm>=4.64.0",
        "Jinja2>=3.0.0"
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"⚠️  Could not install {package}, but this might be optional")
    
    # Download spaCy model
    print("📥 Downloading spaCy model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    # Download NLTK data
    print("📥 Downloading NLTK data...")
    subprocess.run([sys.executable, "-c", "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"])

if __name__ == "__main__":
    install_remaining()