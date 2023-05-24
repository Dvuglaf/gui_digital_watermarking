import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse


def binarization(grayscale: np.array, threshold: float = 0.5) -> np.array:
    grayscale[grayscale >= threshold] = 1.
    grayscale[grayscale < threshold] = 0.
    return grayscale


def get_psnr(coverimage: np.array, marked: np.array) -> float:
    return psnr(coverimage, marked)


def get_ssim(coverimage: np.array, marked: np.array) -> float:
    return ssim(coverimage, marked)


def get_mse(coverimage: np.array, marked: np.array) -> float:
    return mse(coverimage, marked)


def get_ber(watermark: np.array, extracted: np.array) -> float:
    return 100 * np.count_nonzero(watermark - extracted) / (32 * 32)  # in %


def string_to_bitlist(string: str) -> list:
    ords = (ord(c) for c in string)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    return [(o >> shift) & 1 for o in ords for shift in shifts]


def bitlist_to_chars(bitlist: list):
    bitlist = bitlist.astype(np.uint8)
    bititer = iter(bitlist)
    bytes = zip(*(bititer,) * 8)
    shifts = (7, 6, 5, 4, 3, 2, 1, 0)
    for byte in bytes:
        yield chr(sum(bit << s for bit, s in zip(byte, shifts)))


def bitlist_to_string(bitlist: list) -> str:
    return ''.join(bitlist_to_chars(bitlist))


def get_watermark_from_string(string: str) -> np.array:
    bitlist = string_to_bitlist(string)
    watermark = np.zeros(1024, dtype=np.uint8)
    for i in range(len(bitlist)):
        if bitlist[i] == 1:
            watermark[i] = 1
    return watermark.reshape((32, 32))


def get_string_from_watermark(watermark: np.array) -> str:
    return bitlist_to_string(watermark.reshape(1024)).split('\0')[0]

