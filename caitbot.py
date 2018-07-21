#! /usr/bin/python3

import requests
import re

transdict = {"sword" : "Swords", "spear" : "Polearms", "ax" : "Axes",
             "dagger" : "Daggers", "bow" : "Bows", "rod" : "Staves"}
def maketrans(transdict):
    def trans(mo):
        word = mo.group()
        return transdict.get(word.lower(), word)
    return trans

def csv2dict(name):
    head = ["name", "region", "shield", "hp", "weak", "gold",
            "exp", "jp", "item"]
    data = {}
    with open("bestiary.csv", "r") as csv:
        for line in csv:
            if line.startswith(name):
                linesplit = line.split(',')
                info = linesplit[:4]
                info.append(linesplit[4:9])
                info.extend(linesplit[9:])
                data = dict(zip(head,info))
                weaks = " ".join(data["weak"])
                weaks = re.sub("\w+", maketrans(transdict), weaks)
                weaks = re.sub(" N/A", "", weaks)
                data["weak"] = weaks.split()
                return data
def diff(a, b):
    miss = False
    for key, value in a.items():
        if key in b.keys():
            if not (value == b[key]):
                print ("--mismatch: %s [ %s | %s]" % (key, value, b[key]))
                miss = True
    if miss == False:
        print("No misses!")

with open("Cait", "r") as wiki:
    data = {}
    PARSING = False
    for line in wiki:
        if "{{Template:Enemy" in line:
            PARSING = True
        if PARSING:
            if line.startswith("}}"):
                PARSING = False
                continue
            scan = re.findall("\|(.*?)[ =]+(.*?)[\n\|}]", line)
            for item in scan:
                data[item[0]] = item[1]
            if "}}" in line:
                PARSING = False
                continue
    # strip formatting
    for key, value in data.items():
        scan = re.findall("(\w*?)\.png", value)
        if not scan == []:
            data[key] = scan

    a = data
    b = csv2dict("Cait")
    diff (a, b)
