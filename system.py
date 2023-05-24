import skimage
import numpy as np
import tensorflow as tf
from tensorflow import keras
from skimage.io import imshow, show, imread, imsave


def embedding(watermark: np.array, coverimage: np.array) -> np.array:
    embedder = keras.models.load_model("models/embedder_13_visual.h5")
    marked, _, _ = embedder.predict([watermark.reshape((1, 32, 32, 1)), coverimage.reshape((1, 128, 128, 3))])
    return marked.reshape((128, 128, 3))


def extracting(marked: np.array) -> np.array:
    extractor = keras.models.load_model("models/extractor_13_visual.h5")
    extracted, _, _ = extractor.predict([marked.reshape((1, 128, 128, 3))])
    return marked.reshape((128, 128, 3))
