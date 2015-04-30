#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from urllib import quote_plus
from urllib2 import urlopen
from mimetypes import guess_type
from pyquery import PyQuery as pq

def main(word):
    d = pq(url="http://www.onlinedict.com/servlet/MobiDictLookup14?WoRd={0}&example=true&phrase=true&from=prev".format(quote_plus(word)))

    table     = d("table tr:nth-child(2) td")
    moccasin  = table.find("tr[bgcolor=moccasin] td font b").text()
    beige     = table.find("tr[bgcolor=beige] td font b").text()
    next_word = table.find("tr:nth-last-child(5) td a").html();

    print moccasin
    print beige
    print next_word

    # Remove 4 links
    table.remove("tr[bgcolor=moccasin] td[align=center] a")

    # Remove "looking for" keyboard
    table.remove("tr:first-child")

    # Remove last 3 lines
    for i in xrange(0, 5):
        table.remove("tr:last-child")

    # If found PREVIOUS WORD tr, remove again
    if table.find("tr:last-child td").text().find("PREVIOUS WORD") == 0:
        table.remove("tr:last-child")

    # Convert phonetic image to data uri
    for phonetic_img in table.find("tr:nth-child(2) td img"):
        image_tag = pq(phonetic_img)
        image_url = "{0}{1}".format("http://www.onlinedict.com/", image_tag.attr('src').replace("../", ""))

        image_uri = "data:{0};base64,{1}".format(
            guess_type(image_url, strict=True)[0],
            urlopen(image_url).read().encode("base64").replace("\n","")
        )

        image_tag.attr("src", image_uri)

    # Save html
    # with open("./{0}.html".format(word), 'w+') as f:
    #     f.write(table.html().encode("utf-8"))
    #     f.close()

def create_database():
    from models import Word

    Word.create_table()

if __name__ == "__main__":
    # create_database()

    main("door")
