# Extract everything if not extracted

# Check all the flags to make sure I don't set one used by the game
import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

EXTRACT_ARDS=False


arddir = os.path.join(os.environ["KHGAMES_PATH"],"KH2", "subfiles", "script", "ard")
if EXTRACT_ARDS:    
    if os.path.exists(arddir):
        shutil.rmtree(arddir)
    os.mkdir(arddir)

spawndir = os.path.join(os.getcwd(), "spawnscripts")
if os.path.exists(spawndir):
    shutil.rmtree(spawndir)
os.mkdir(spawndir)

ardinfo = {}
ignore_worlds = [
]
ignore_ards = [
    "hb02.ard", #1K site
    "lk12.ard", # overlook
    "mu05.ard", # cave
    "mu07.ard", #summit
    "al10.ard", #treasure room
    "dc00.ard", #audience chamber
    "he09.ard", #cups
]
# These issues might all be related to GOA mod
# I need to know if there are any areas in the game where a mission starts without a cutscene beforehand
ignore_programs = {

}


CAPACITY = "-3.3895395E+38"
unskippable = []
ignored = []
def getCustomJump(ard, program,line):
    if ard in custom_jumps:
        if program in custom_jumps[ard]:
            print("custom jumping over: {}".format(line))
            return custom_jumps[ard][program]
    return False

def shouldIgnore(ard, program):
    global ignored
    ignore = False
    if ard[:2] in ignore_worlds:
        ignore = True
    if ard in ignore_ards:
        ignore = True
    if ard in ignore_programs:
        if program.strip() in ignore_programs[ard]:
            ignore = True
    if ignore:
        ignored.append("{}-{}".format(ard,program.strip()))
    return ignore

arddir_src = os.path.join(os.environ["KHGAMES_PATH"], "KH2", "KH2","ard")

noevtinventory = []
eventpresent=False
last_asetting = ''
asettings = {}
eventtypes = []
for ard in os.listdir(arddir_src):
    btlname = None
    fn = os.path.join(arddir_src, ard)

    out_pth = os.path.join(arddir, ard.split(".")[0])
    if EXTRACT_ARDS:
        lib.editengine.bar_extract(fn, out_pth)
    
    if "btl.script" in os.listdir(out_pth):
        btlname = "btl.script"

    ardinfo[ard] = {
        "fn": fn,
        "out_pth": out_pth
    }
    if btlname == None:
        print("ARD {} has no btl".format(ard))
    else:

        btl_pth = os.path.join(out_pth, btlname)
        if EXTRACT_ARDS:
            lib.editengine.spawnscript_extract(btl_pth, btl_pth)
        
        lines = open(btl_pth)
        lines_program_vanilla = []
        lines_new = []
        currentProgram = ''
        lines_program = []
        changesMade = False
        setsinventory = False
        for line in lines:
            if line.startswith("Program"):
                if len(currentProgram) > 0:
                    if changesMade:
                        spawnscriptsdir = os.path.join(spawndir, ard)
                        if not os.path.exists(spawnscriptsdir):
                            os.mkdir(spawnscriptsdir)
                        programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
                        with open(programfn, "w") as f:
                            f.write(''.join(lines_program_vanilla if setsinventory else lines_program))
                    lines_program = []
                    lines_program_vanilla = []
                    changesMade = False
                    eventpresent = False
                    setsinventory = False
                currentProgram = line.split(" ")[1]
            if len(currentProgram) > 0:
                if "Capacity" in line and not shouldIgnore(ard, currentProgram):
                    newline = ' '.join(line.split(" ")[:-1])+" "+CAPACITY+"\n"
                    changesMade=True
                    lines_program.append(newline)
                    lines_program_vanilla.append(newline)
                else:
                    lines_program_vanilla.append(line)
                    lines_program.append(line)
                    lines_new.append(line)
        # Changes made here need to happen up above too
        if changesMade:
            spawnscriptsdir = os.path.join(spawndir, ard)
            if not os.path.exists(spawnscriptsdir):
                os.mkdir(spawnscriptsdir)
            programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
            with open(programfn, "w") as f:
                f.write(''.join(lines_program))
        open(btl_pth+".txt.new","w").write("".join(lines_new))
print(ignored)
# print(noevtinventory)
# Print out all the ards with a letter in the