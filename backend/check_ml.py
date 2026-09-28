try:
    import cv2
    print("OpenCV version:", cv2.__version__)
except ImportError as e:
    print("OpenCV not installed:", e)

try:
    import tensorflow as tf
    print("TensorFlow version:", tf.__version__)
except ImportError as e:
    print("TensorFlow not installed:", e)

try:
    import numpy as np
    print("NumPy version:", np.__version__)
except ImportError as e:
    print("NumPy not installed:", e)
