#! /usr/bin/env python3
# Copyright (c) 2020 Slavfox
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from urllib import request
from lxml import html
from urllib.request import urlopen
import base64

basepath = (
    "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)"
)


def get_villager_rows():
    with request.urlopen(basepath) as resp:
        villagerlist_body = resp.read()
    tree = html.fromstring(villagerlist_body)
    villager_rows = tree.xpath('//table[//a[@title="Villagers"]]//table/tr')
    return villager_rows


def get_villagers():
    rows = get_villager_rows()
    villagers = {}
    for row in rows:
        tds = row.xpath("./td")
        try:
            name, image, personality, species, birthday, catchphrase = tds
        except ValueError:
            continue

        name = name.xpath(".//a")[0].text.strip()
        print(name)
        image = image.xpath(".//a")[0].attrib["href"]
        image = base64.encodebytes(urlopen(image).read()).decode('ascii')
        personality = personality.xpath(".//a")[0].text.split()[-1].lower()

        catchphrase = catchphrase.xpath(".//i")[0].text.strip().strip('"')
        villagers.setdefault(personality, []).append(
            [name, image, catchphrase]
        )
    return villagers


if __name__ == "__main__":
    from json import dump

    with open("villager_dump.json", "w") as f:
        dump(get_villagers(), f, indent=2)

    print("Rename villager_dump.json to villagers.json")
