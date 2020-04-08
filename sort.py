#! /usr/bin/env python3
# Copyright (c) 2020 Slavfox
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import random
import tkinter as tk
from pathlib import Path

with open("villagers.json") as f:
    villagers = json.load(f)

def init_queue(personality):
    total = 0
    queue = []
    for v1 in villagers[personality]:
        for v2 in villagers[personality]:
            if v1[0] != v2[0] and (v2[0], v1[0]) not in queue:
                queue.append((v1[0], v2[0]))
                total += 1
    random.shuffle(queue)
    return total, queue


class Sorter(tk.Frame):
    def __init__(self):
        master = tk.Tk()
        super().__init__(master)
        self.villager_info = {}
        for l in villagers.values():
            for v in l:
                self.villager_info[v[0]] = (tk.PhotoImage(data=v[1]), v[2])

        self.total = 0
        if Path('ratings.json').is_file():
            with open('ratings.json') as f:
                data = json.load(f)
                self.ratings = data["ratings"]
                self.queue = data["queue"]
                self.battleno = data["battleno"]
                self.total = data["total"]
        else:
            self.ratings = {v: 0 for v in self.villager_info}
            self.battleno = 0
            self.queue = {}
            for p in villagers:
                t, pq = init_queue(p)
                self.total += t
                self.queue[p] = pq

        self.v1 = None
        self.v2 = None
        self.personality = None
        self.iterator = self.iterbattles()

        self.master = master
        self.pack()
        self.battlelabel = tk.Label(
            self, text=f"Battle {self.battleno}/{self.total}"
        )
        self.battlelabel.pack(side="top")
        self.personalitylabel = tk.Label(self, text="personality")
        self.personalitylabel.pack(side="top")
        self.left = tk.Frame(self)
        self.left.pack(side="left")
        self.right = tk.Frame(self)
        self.right.pack(side="right")

        self.leftlabel = tk.Label(self.left, text="Villager 1")
        self.leftlabel.pack()
        self.leftcv = tk.Canvas(self.left, bg="white", width=128, height=128)
        self.leftcv.pack()
        self.leftcatchprase = tk.Label(self.left, text="Catchprase 1")
        self.leftcatchprase.pack()
        self.choose_left = tk.Button(self.left, text="+1",
                                 command=self.click_choose_left)
        self.choose_left.pack()
        self.never_left = tk.Button(self.left, text="Fuck off",
                                 command=self.click_never_left)
        self.never_left.pack()

        self.rightlabel = tk.Label(self.right, text="Villager 2")
        self.rightlabel.pack()
        self.rightcv = tk.Canvas(self.right, bg="white", width=128, height=128)
        self.rightcv.pack()
        self.rightcatchprase = tk.Label(self.right, text="Catchprase 2")
        self.rightcatchprase.pack()
        self.choose_right = tk.Button(self.right, text="+1",
                                 command=self.click_choose_right)
        self.choose_right.pack()
        self.never_right = tk.Button(self.right, text="Fuck off",
                                 command=self.click_never_right)
        self.never_right.pack()


        self.no_opinion = tk.Button(self, text="No opinion",
                                 command=self.click_no_opinion)
        self.no_opinion.pack(side="bottom")

        self.next()

    def click_choose_left(self):
        self.ratings[self.v1] += 2
        self.next()

    def click_never_left(self):
        self.fuck_off(self.v1)
        self.next()

    def click_choose_right(self):
        self.ratings[self.v2] += 2
        self.next()

    def click_never_right(self):
        self.fuck_off(self.v2)
        self.next()

    def fuck_off(self, who):
        for q in self.queue.values():
            indices = []
            for i in reversed(range(len(q))):
                if q[i][0] == who:
                    self.ratings[q[i][1]] += 2
                    indices.append(i)
                elif q[i][1] == who:
                    self.ratings[q[i][0]] += 2
                    indices.append(i)
            for i in indices:
                del q[i]
                self.total -= 1

    def click_no_opinion(self):
        self.ratings[self.v1] += 1
        self.ratings[self.v2] += 1
        self.next()

    def next(self):
        self.save()
        next(self.iterator)

    def save(self):
        tmp = Path('ratings.sav.json')
        with tmp.open("w") as f:
            json.dump(
                {"ratings": self.ratings, "queue": self.queue, "battleno":
                    self.battleno, "total": self.total},
                f
            )
        tmp.rename("ratings.json")

    def iterbattles(self):
        for p, q in list(self.queue.items()):
            self.personality = p
            self.personalitylabel["text"] = p
            while q:
                self.battleno += 1
                v1, v2 = q[-1]
                self.v1 = v1
                self.v2 = v2
                imagedata1, catchphase1 = self.villager_info[v1]
                imagedata2, catchphase2 = self.villager_info[v2]
                self.battlelabel["text"] = f"Battle {self.battleno}/{self.total}"
                self.leftlabel["text"] = v1
                self.leftcatchprase["text"] = catchphase1
                self.leftcv.create_image(0, 0, image=imagedata1, anchor="nw")
                self.rightlabel["text"] = v2
                self.rightcatchprase["text"] = catchphase2
                self.rightcv.create_image(0, 0, image=imagedata2, anchor="nw")
                yield
                q.pop()
            del self.queue[p]


if __name__ == '__main__':

    app = Sorter()
    app.mainloop()
