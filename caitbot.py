#! /usr/bin/python3

import requests
import re
import sys

transdict = {"sword" : "Swords", "spear" : "Polearms", "ax" : "Axes",
             "dagger" : "Daggers", "bow" : "Bows", "rod" : "Staves"}
def maketrans(transdict):
    def trans(mo):
        word = mo.group()
        return transdict.get(word.lower(), word)
    return trans

def csv2dict(name):
    head = ["name", "shield", "hp", "weak", "gold",
            "exp", "jp", "item"]
    data = {}
    try:
        with open("bestiary.csv", "r") as csv:
            for line in csv:
                if line.startswith(name):
                    linesplit = line.split(',')
                    info = linesplit[:3]
                    info.append(linesplit[3:8])
                    info.extend(linesplit[8:])
                    data = dict(zip(head,info))
                    weaks = " ".join(data["weak"])
                    weaks = re.sub("\w+", maketrans(transdict), weaks)
                    weaks = re.sub(" N/A", "", weaks)
                    data["weak"] = weaks.split()
                    return data
    except FileNotFoundError:
        print("Bestiary not found!")
        print("Did you download it?")
        print(" -> clone-sheet")
        sys.exit()

def diff(a, b):
    miss = False
    for key, value in a.items():
        if key in b.keys():
            if not (value == b[key]):
                print ("--mismatch: %s [ %s | %s]" % (key, value, b[key]))
                miss = True
    if miss == False:
        print("No misses!")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please select an enemy to match")
        sys.exit()
    else:
        r = requests.get("https://octopathtraveler.wikia.com/wiki/" +
                         "_".join(sys.argv[1:]) +
                         "?action=raw")
        wiki = r.text.split('\n')
        data = {}
        PARSING = False
        for line in wiki:
            if any(x in line for x in ["{{Template:Enemy",
                                       "{{Template:Character"]):
                PARSING = True
            if PARSING:
                if line.startswith("}}"):
                    PARSING = False
                    continue
                scan = re.findall("\|(.*?)[ =]+(\w*)", line)
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
        b = csv2dict(" ".join(sys.argv[1:]))
        diff (a, b)
