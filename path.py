import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import os
sys.setrecursionlimit(9999)
inpt1 = sys.argv[1]

blank = "100"
wall = "0"

mazel = []
with open(inpt1,"r") as file:
    row = 0
    for line in file:
        templ = []
        col = 0
        for char in line:
            if char != "\n":
                if char == "F" or char == "S":
                    templ.append(char + (len(blank)-1)*blank[0])
                elif char == "P":
                    templ.append(blank)
                elif char == "W":
                    templ.append(wall)
            if char == "F":
                fx,fy = col,row

            if char == "S":
                sx,sy = col,row
            col += 1
        ma_col = col
        row += 1
        mazel.append(templ)
    ma_row = row
    pic = np.full((ma_col-1,ma_row),0)

print(f"START  {sx},{sy}   --- FINISH {fx},{fy}")
print(ma_col,ma_row)

def around(x,y,p):
    u,d,l,r = False,False,False,False
    if y != 0:
        if mazel[y-1][x] == blank or mazel[y-1][x] == "F"+(len(blank)-1)*blank[0] or mazel[y-1][x] == "H"+(len(blank)-1)*blank[0]:
            if (x,y-1) not in p:
                u = True
    if y != (len(mazel)-1):
        if mazel[y+1][x] == blank or mazel[y+1][x] == "F"+(len(blank)-1)*blank[0] or mazel[y+1][x] == "H"+(len(blank)-1)*blank[0]:
            if (x,y+1) not in p:
                d = True
    if x != (len(mazel[0])-1):
        if mazel[y][x+1] == blank or mazel[y][x+1] == "F"+(len(blank)-1)*blank[0] or mazel[y][x+1] == "H"+(len(blank)-1)*blank[0]:
            if (x+1,y) not in p:
                r = True
    if x != 0:
        if mazel[y][x-1] == blank or mazel[y][x-1] == "F"+(len(blank)-1)*blank[0] or mazel[y][x-1] == "H"+(len(blank)-1)*blank[0]:
            if (x-1,y) not in p:
                l = True
    #print(list(zip(("UP","DOWN","LEFT","RIGHT"),(u,d,l,r))),"\n")
    return (u,d,l,r)


vis = []
path = []
success_path = []

stime = time.time()
def li_copier(f):
    temp = []
    t = []
    for i in f:
        t.append(i[:])
    return t
takenpath = 0
def print_m(using,sym):
    global takenpath
    global aaa
    tempm = li_copier(mazel)
    tempm[sy][sx] = 200
    tempm[fy][fx] = 200
    for i,j in using:
        if tempm[j][i] == blank:
            tempm[j][i] = sym
    a = np.array(tempm, dtype=int)
    plt.pcolor(a,cmap="inferno")
    plt.tight_layout()
    plt.axis("off")
    plt.savefig(f"{len([name for name in os.listdir('.') if os.path.isfile(name)])}.png")
    plt.clf()
    takenpath += 1


def solver(start,finish,taken):
    x,y = start
    branch = taken[:]
    branch.append(start)
    if start != (fx,fy):
        vis.append(start)
    print_m(branch,175)
    print(len([name for name in os.listdir('.') if os.path.isfile(name)]))
    #print("----",branch)
    if start == finish:
        #print("Solution found!")
        #print(branch)
        success_path.append(branch[:])
    else:
        #print(x,y)
        u,d,l,r = around(x,y,vis)
        if d:
            solver((x,y+1),finish,branch)
        if r:
            solver((x+1,y),finish,branch)
        if l:
            solver((x-1,y),finish,branch)
        if u:
            solver((x,y-1),finish,branch)


solver((sx,sy),(fx,fy),path)
min_path = success_path[0]
for i in success_path:
    if len(i) < len(min_path):
        min_path = i
print(takenpath)
