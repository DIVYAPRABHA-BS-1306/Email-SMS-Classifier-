print("Testing imports...")

try:
    import pandas as pd
    print("✅ Pandas imported successfully")
except ImportError as e:
    print(f"❌ Pandas error: {e}")

try:
    import numpy as np
    print("✅ NumPy imported successfully")
except ImportError as e:
    print(f"❌ NumPy error: {e}")

try:
    import sklearn
    print("✅ Scikit-learn imported successfully")
except ImportError as e:
    print(f"❌ Scikit-learn error: {e}")

try:
    import nltk
    print("✅ NLTK imported successfully")
except ImportError as e:
    print(f"❌ NLTK error: {e}")

print("Import test completed.")