#!/usr/bin/env python3
# Copyright (c) 2020 Slavfox
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
villager_ratings = []
personality_ratings = {}
with open("ratings.json") as f:
    ratings = json.load(f)["ratings"]
with open("villagers.json") as f:
    villagers = json.load(f)

personality_max = {}
for p, vs in villagers.items():
    personality_max[p] = max(ratings[v[0]] for v in vs)

for p, vs in villagers.items():
    rs = []
    for v in vs:
        r = (ratings[v[0]]+1) / (personality_max[p]+1)
        rs.append((v[0], r))
        villager_ratings.append((v[0], r))
    personality_ratings[p] = sorted(rs, key=lambda x: x[1], reverse=True)
villager_ratings = sorted(villager_ratings, key=lambda x: x[1], reverse=True)


selected = set()
print("Best villager per personality:")
print("==============================")
for p in personality_ratings:
    v = personality_ratings[p][0][0]
    print(f"{p.capitalize()}: {v}")
    selected.add(v)

print("\nThe best picks to fill out your island are:")
picks = []
for v in villager_ratings:
    if v[0] not in selected:
        picks.append(v[0])
        if len(picks) >= 10:
            break

for i, v in enumerate(picks):
    print(f"{i}. {v}")
