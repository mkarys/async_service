import io
import sys

import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.crypto import get_random_string
from PyDictionary import PyDictionary
from wordcloud import WordCloud


def get_related_words(keyword):
    dictionary = PyDictionary()

    related_words = []
    for single_word in keyword.split(" "):
        synonyms = dictionary.synonym(single_word)
        if synonyms is not None:
            related_words.append(", ".join(synonyms))
    return ", ".join(related_words)


def create_image_for_words(keyword, related_words):
    text = f"{keyword}, {related_words}"

    x, y = np.ogrid[:300, :300]

    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    wc = WordCloud(background_color="black", repeat=True, mask=mask)
    wc.generate(text)
    image = wc.to_image()

    output = io.BytesIO()
    image.save(output, format="JPEG", quality=85)
    output.seek(0)
    return InMemoryUploadedFile(
        output,
        "ImageField",
        get_random_string(16),
        "image/jpeg",
        sys.getsizeof(output),
        None,
    )
