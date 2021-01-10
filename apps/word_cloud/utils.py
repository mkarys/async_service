import asyncio
import io
import sys

import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.crypto import get_random_string
from PyDictionary import PyDictionary
from wordcloud import WordCloud

from apps.word_cloud.async_py_dictionary import AsyncPyDictionary


def run_async(word_cloud):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    related_words, image = loop.run_until_complete(
        async_generate_cloud_word(word_cloud.keyword)
    )
    loop.close()

    return related_words, image


def run_sync(word_cloud):
    related_words, image = generate_cloud_word(word_cloud.keyword)
    return related_words, image


async def async_generate_cloud_word(keyword):
    related_words = await async_get_related_words(keyword)
    image = await async_create_image_for_words(keyword, related_words)
    return related_words, image


async def async_create_image_for_words(keyword, related_words):
    return create_image_for_words(keyword, related_words)


async def async_get_related_words(keyword):
    dictionary = AsyncPyDictionary()
    tasks = []
    for single_word in keyword.split(" "):
        tasks.append(asyncio.create_task(dictionary.synonym(single_word)))
        tasks.append(asyncio.create_task(dictionary.antonym(single_word)))

    results = await asyncio.gather(*tasks)
    related_words = [item for sublist in results for item in sublist]
    return ", ".join(related_words)


def generate_cloud_word(keyword):
    related_words = get_related_words(keyword)
    image = create_image_for_words(keyword, related_words)
    return related_words, image


def get_related_words(keyword):
    dictionary = PyDictionary()

    related_words = []
    for single_word in keyword.split(" "):
        synonyms = dictionary.synonym(single_word)
        antonyms = dictionary.antonym(single_word)
        if synonyms is not None:
            related_words.append(", ".join(synonyms))
        if antonyms is not None:
            related_words.append(", ".join(antonyms))
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
