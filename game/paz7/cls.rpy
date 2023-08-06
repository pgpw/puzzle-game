init -2 python:
    class Pazl(python_object):#============================== КЛАСС ПАЗЛОВ ======================================================
        __slots__ =("xpos","ypos","xintpos","yintpos","xtarget","ytarget","xspeed","yspeed","speed","steps",
            "IMG","XNUM","YNUM")
        def __init__(self,xpos=100,ypos=100,xtarget=1,ytarget=1,xspeed=0,yspeed=0,speed=20,steps=0,
            IMG=0,
            XNUM=0,YNUM=0,):
            #-------------------- ПОЛОЖЕНИЕ В ПРОСТРАНСТВЕ
            self.xpos=0                    #
            self.ypos=0                    #
            self.xintpos=xpos                 #
            self.yintpos=ypos                 #
            self.xtarget=0                 #
            self.ytarget=0                 #
            self.xspeed=0
            self.yspeed=0
            self.speed=20
            self.steps=0
            #-------------------- КОНСТАНТЫ
            self.IMG=IMG                   #
            #-------------------- НОМЕР В МАТРИЦЕ
            self.XNUM=XNUM
            self.YNUM=YNUM
##########################################################################################################################
    class Pazgame(python_object):#====================== КЛАСС ИГРЫ =================================================================
        __slots__ =("movecard","cardwalkback","dropcard","hovercard","cardnumb","gameover",
            "pazsklad","pazbar","paztab","bg",
            "BARYPOZ","BARXPOZ")
        def __init__(self,bg="a/paz7/ui/bg.png"):
            self.movecard=0
            self.cardwalkback=0
            self.dropcard=0
            self.hovercard=-1
            self.cardnumb=-1
            self.gameover=0
            #--------------------------
            self.pazsklad=[]
            self.pazbar=[]
            self.paztab=[]
            self.bg=bg
            #-------------------------
            self.BARYPOZ=[20,240,460,680]
            self.BARXPOZ=1600
        def cardhit(self,q):#===========================  ====================================
            for i in self.pazmatrix:
                if z in i:
                    if not z:
                        movecard.ytarget=1
                        movecard.xtarget=1
        def play(self):#===================== ОСНОВНАЯ ФУНКЦИЯ ИГРЫ ===============================================
            if len(self.pazbar)<4:
                for n,i in enumerate(range(4-len(self.pazbar))):
                    if self.pazsklad:
                        paz=self.pazsklad.pop()
                        paz.yintpos=self.BARYPOZ[3-n]
                        paz.xintpos=self.BARXPOZ
                        paz.ytarget=paz.yintpos
                        paz.xtarget=paz.xintpos
                        self.pazbar.append(paz)
            if self.movecard:
                if self.cardwalkback:
                    self.card_walkback(self.movecard)
                    if not self.cardwalkback:
                        self.movecard.xintpos=self.movecard.xtarget
                        self.movecard.yintpos=self.movecard.ytarget
                        self.movecard=0
                        return
                    self.movecard.xintpos=int(self.movecard.xpos)
                    self.movecard.yintpos=int(self.movecard.ypos)
                    return
                elif self.dropcard:
                    cell=self.cardhit(self.movecard)
                    if cell:
                        self.hitmonster(cell,self.cardlist.pop(self.cardnumb))
                    else:
                        self.cardwalkback=1
                        self.xyspeed(self.movecard)
                    self.dropcard=0
                    self.cardnumb=-1
                    return
                self.movecard.xpos,self.movecard.ypos=MOUSEPOS()
                self.movecard.xintpos=int(self.movecard.xpos)
                self.movecard.yintpos=int(self.movecard.ypos)
        def pazcreate(self,img,num):#================== СОЗДАЁМ ФРАГМЕНТЫ ======================================
            lis=[]
            pazsize=200
            for x in range(8):
                for y in range(5):
                    lis.append(Pazl(IMG="p{}x{}y{}".format(num,x,y),XNUM=x,YNUM=y))
                    
                    renpy.image(lis[-1].IMG,Crop((x*pazsize,y*pazsize,pazsize,pazsize),img))
            return lis
        def card_walkback(self,q):#=========== ВОЗВРАЩЕНИЕ ФРАГМЕНТА =================================
            q.xpos=q.xpos+q.xspeed
            q.ypos=q.ypos+q.yspeed
            if q.steps:
                q.steps=max(0,q.steps-1)
                return
            self.cardwalkback=0
        def xyspeed(self,q):#====================== РАСЧЁТ СКОРОСТИ БОЛИДА ======================================
            xnegative=0
            ynegative=0
            if q.xpos>q.xtarget:# НАХОДИМ Х КАТЕТ
                xkat=q.xpos-q.xtarget
                xnegative=1
            else:
                xkat=q.xtarget-q.xpos
            if q.ypos>q.ytarget:# НАХОДИМ У КАТЕТ
                ykat=q.ypos-q.ytarget
                ynegative=1
            else:
                ykat=q.ytarget-q.ypos
            gipot=sqrt(xkat**2+ykat**2)          # НАХОДИМ ГИПОТЕНУЗУ
            xproc=xkat/float(gipot)              # НАХОДИМ ПРОЦЕНТ СООТНОШЕНИЕ Х К ГИПОТЕНУЗЕ
            yproc=ykat/float(gipot)              # НАХОДИ ПРОЦЕНТ СООТНОШЕНИЕ У К ГИПОТЕНУЗЕ
            if xnegative:
                q.xspeed=-q.speed*xproc          # НАХОДИМ СКОРОСТЬ ДВИЖЕНИЯ ПО Х
            else:
                q.xspeed=q.speed*xproc
            if ynegative:
                q.yspeed=-q.speed*yproc
            else:
                q.yspeed=q.speed*yproc                # НАХОДИМ СКОРСТЬ ДВИЖЕНИЯ ПО У
            if q.xspeed:                              # НАХОДИМ КОЛИЧЕСТВО ШАГОВ ДО ЦЕЛИ
                q.steps=int(abs(xkat)/abs(q.xspeed))
            else:
                q.steps=int(abs(ykat)/abs(q.yspeed))
        def __call__(self,x):#================= ЗАПУСКАЮЩАЯ МИНИ ИГРУ ФУНКЦИЯ ======================================================
            global quick_menu,pazgame
            pazgame=Pazgame()
            pazgame.pazsklad=deepcopy(ALLPAZFRAG[x])
            quick_menu=False
            renpy.choice_for_skipping()
            renpy.call("paz_start")