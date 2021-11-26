# from bs4 import BeautifulSoup, Comment
import justext
import html2text
import trafilatura
# import dragnet
import re


class Parser:
    """Custom parser class to try different parsers """

    def trafilatura(self, html):

        text = trafilatura.extract(html)
        return text


    def justext(self, html):
        text = ""
        paragraphs = justext.justext(html, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                text += paragraph.text

        if not text:
            # print("no text found")
            Exception("No text")

        return text

    # def beautiful_soup(self, html):

    #     soup = BeautifulSoup(html, "html.parser")

    #     # Try more advanced techniques here.
    #     for data in soup(["style", "script", "aside", "footer"]):
    #         # Remove tags
    #         data.extract()

    #     # return data by retrieving the tag content
    #     text = " ".join(re.split(r"[\n\t]+", soup.get_text())).replace(".", "")

    #     return text

    # def dragnet(self, html):
    #     text = dragnet.extract(html)
    #     return text
