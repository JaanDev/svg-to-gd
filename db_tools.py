import datetime

import gd
from gd.api import *

NAME = "SVG To GD(generated)"


def add_level(new_lvl: Editor):
    print(f"Adding objects to a level called \"{NAME}\"(might take a while)")
    t = datetime.datetime.now()

    db = save.load()
    levels = db.get_created_levels()

    lvl = LevelAPI()
    lvl.set_data(new_lvl.dump())
    lvl.level_type = gd.LevelType.EDITOR
    lvl.name = NAME

    for l in levels:
        if l.name == NAME:
            levels.remove(l)

    levels.insert(0, lvl)

    db.dump_created_levels(levels)
    db.dump()

    print("Done in " + str(datetime.datetime.now() - t).split(".")[0] + ". Objects: " + str(len(new_lvl.objects)))
