import pgzrun
import random as rd

TITLE = 'JumpFun'
WIDTH = 500
HEIGHT = 700

count = 0
score = 0
fail = False
tmout = False
dudu = Actor('嘟嘟')
bricks = []
motion = {}
for i in range(5):
    b = Actor('踏板'+str(rd.randint(1,3)))
    b.x = rd.randint(b.width//2,500-b.width//2)
    b.y = 140*(i+1)+100
    bricks.append(b)
    if i == 2:
        dudu.x = b.x
        dudu.bottom = b.top
try:
    with open('Data.db','r') as Date:
        best = int(''.join([chr(int(i)) for i in Date.readline().split()]))
except:
    best = 0

def draw():
    global score
    screen.blit('背景',[0,0])
    screen.draw.text('Score:'+str(score),(25,15),fontsize=30,color='cyan')
    screen.draw.text('Best:'+str(best),(400,15),fontsize=30,color='blue')
    dudu.draw()
    for b in bricks:
        b.draw()
    if fail or tmout:
        screen.fill("Silver")
        screen.draw.text(('FAIL!' if fail else 'Time Out'),(191 if fail else 150,200),fontsize=70,color='red')
        screen.draw.text('Score:'+str(score)+'\t'+'Best:'+str(best),(130,280),fontsize=40,color='cyan')
        screen.draw.text('Press Space To '+('Try Again' if fail else 'Go On'),(40 if fail else 70,350),fontsize=50)

def update():
    global fail,score,count,motion,best
    if not (fail or tmout):
        for b in bricks:
            b.y -= score/50+1
            if b.y < 0:
                if b in motion.keys():
                    del motion[b]
                b.y = 700
                if count < 2:
                    b.image = '踏板'+str(rd.randint(1,rd.randint(3,4)))
                    if b.image == '踏板4':
                        count += 1
                else:
                    b.image = '踏板'+str(rd.randint(1,3))
                    count = 0
                b.x = rd.randint(b.width//2,500-b.width//2)
                if rd.randint(1,(2 if 200-score<=2 else 200-score)) == 1 and b.image != '踏板4':
                    motion[b] = rd.randint(0,1)
                score += 1
            elif dudu.colliderect(b) and dudu.bottom-b.top < 10+score// 10:
                if not keyboard.down or dudu.image == '嘟嘟哭':
                    dudu.bottom = b.top
                if b.image == '踏板4':
                    dudu.image = '嘟嘟哭'
            else:
                dudu.y += 1
        for b in motion.keys():
            if motion[b]:
                b.x -= 2
                if b.left < 0:
                    motion[b] = 0
            if not motion[b]:
                b.x += 2
                if b.right > 500:
                    motion[b] = 1
        if dudu.image != '嘟嘟哭':
            if keyboard.left and dudu.left > 0:
                dudu.x -= 5
            if keyboard.right and dudu.right < 500:
                dudu.x += 5
        if score > best:
            best = score
            with open('Data.db','w') as Date:
                Date.write(' '.join('%s'%i for i in [ord(i) for i in str(best)]))
        if dudu.top > 700 or dudu.bottom < 0:
            fail = True

def on_key_down(key):
    global count,score,fail,motion,tmout
    if key == keys.SPACE:
        if fail:
            count = 0
            score = 0
            fail = False
            tmout = False
            motion = {}
            dudu.image = '嘟嘟'
            i = 0
            for b in bricks:
                b.image = '踏板'+str(rd.randint(1,3))
                b.x = rd.randint(b.width//2,500-b.width//2)
                b.y = 140*(i+1)+100
                if i == 2:
                    dudu.x = b.x
                    dudu.bottom = b.top
                i += 1
        else:
            tmout = True if not tmout else False

pgzrun.go()
