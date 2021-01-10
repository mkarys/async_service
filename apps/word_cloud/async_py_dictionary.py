import aiohttp
import requests
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary


class AsyncPyDictionary(PyDictionary):
    @staticmethod
    async def synonym(term, formatted=False):
        if len(term.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
            try:
                data = await _get_soup_object(
                    "https://www.synonym.com/synonyms/{0}".format(term)
                )
                section = data.find("div", {"class": "type-synonym"})
                spans = section.findAll("a")
                synonyms = [span.text.strip() for span in spans]
                if formatted:
                    return {term: synonyms}
                return synonyms
            except AttributeError:
                print("{0} has no Synonyms in the API".format(term))
                return []

    @staticmethod
    async def antonym(term, formatted=False):
        if len(term.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
            try:
                data = await _get_soup_object(
                    "https://www.synonym.com/synonyms/{0}".format(term)
                )
                section = data.find("div", {"class": "type-antonym"})
                spans = section.findAll("a")
                antonyms = [span.text.strip() for span in spans]
                if formatted:
                    return {term: antonyms}
                return antonyms
            except AttributeError:
                print("{0} has no Antonyms in the API".format(term))
                return []


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def _get_soup_object(url, parser="html.parser"):
    async with aiohttp.ClientSession() as session:
        response_text = await fetch(session, url)
        return BeautifulSoup(response_text, parser)
