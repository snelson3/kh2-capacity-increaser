import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

TITLE = "KH2 Capacity Increaser"

spawndir = os.path.join("spawnscripts")

assets = []

for ard in os.listdir(spawndir):
    programs = []
    for fn in os.listdir(os.path.join(spawndir, ard)):
        programs.append(os.path.join(spawndir, ard, fn))

        
    a = {
        "name": "ard/{}".format(ard),
        "method": "binarc",
        "source": [
            {
                "name": "btl",
                "type": "AreaDataScript",
                "method": "areadatascript",
                "source": [            
                    {
                        "name": programs[i].replace("\\", "/"),
                    }
                    for i in range(len(programs))
                ]
            }
        ]
    }

    assets.append(a)
mod = {
    "originalAuthor": "Thundrio",
    "description": """READ THIS FIRST
Sets the capacity for all the battles that set capacity to an arbitrarily large number, in order to eliminate issues with spawn limiters
may cause crashes in certain cases. Some areas that are more likely to crash have been excluded""",
    "title": TITLE,
    "assets": assets
}
import yaml
yaml.dump(mod, open("mod.yml", "w"))