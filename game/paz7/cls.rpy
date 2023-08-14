init -2 python:
    class Pazl(python_object):#============================== КЛАСС ПАЗЛОВ ======================================================
        __slots__ =("xpos","ypos","xintpos","yintpos","xtarget","ytarget","xspeed","yspeed","speed","steps",
            "xbox","ybox",
            "xmatrix","ymatrix",
            "place",
            "IMG","XNUM","YNUM")
        def __init__(self,xpos=0,ypos=-300,xtarget=1,ytarget=1,xspeed=0,yspeed=0,speed=20,steps=0,
            IMG=0,
            XNUM=0,YNUM=0,):
            #-------------------- ПОЛОЖЕНИЕ В ПРОСТРАНСТВЕ
            self.xpos=0                    #
            self.ypos=0                    #
            self.xintpos=xpos              #
            self.yintpos=ypos              #
            self.xtarget=0                 #
            self.ytarget=0                 #
            self.xspeed=0
            self.yspeed=0
            self.speed=40
            self.steps=0
            #--------------------
            self.xbox=200
            self.ybox=200
            #-------------------
            self.xmatrix=0
            self.ymatrix=0
            #-------------------
            self.place=0
            #-------------------- КОНСТАНТЫ
            self.IMG=IMG                   #
            #-------------------- НОМЕР В МАТРИЦЕ
            self.XNUM=XNUM
            self.YNUM=YNUM
##########################################################################################################################
    class Pazgame(python_object):#====================== КЛАСС ИГРЫ ======================================================
        __slots__ =("movecard","cardwalkback","dropcard","hovercard","cardnumb","gameover",
            "pazmatrix","pazpoint","xmtrsize","ymtrsize","pazbarsize",
            "pazlist","pazsklad","pazbar","paztab","bg",
            "BARYPOZ","BARXPOZ")
        def __init__(self,bg="a/paz7/ui/bg.png"):
            self.movecard=0
            self.cardwalkback=0
            self.dropcard=0
            self.hovercard=-1
            self.cardnumb=-1
            self.gameover=0
            #-------------------------- МАТРИЦЫ ПАЗЛОВ
            self.pazmatrix=[]
            self.pazpoint=[]
            self.xmtrsize=0
            self.ymtrsize=0
            self.pazbarsize=5
            #-------------------------- ЛИСТЫ ПАЗЛОВ
            self.pazlist=[]
            self.pazsklad=[]
            self.pazbar=[]
            self.paztab=[]
            self.bg=bg
            #------------------------- КОНСТАНТЫ
            self.BARYPOZ=[10,220,430,640,850]
            self.BARXPOZ=1660
        def cardhit(self,q):#===================== ПОИСК ЯЧЕЙКИ И ПРОВЕРКА СВОБОДНОСТИ  ==================================
            xintpos=q.xintpos+100
            yintpos=q.yintpos+100
            if xintpos>self.xmtrsize*q.xbox or yintpos>self.ymtrsize*q.ybox:# КОГДА БРОСАЕМ МИМО ЯЧЕЙКИ
                if q.place is 2:
                    q.place=0
                    xtarget=pazgame.BARXPOZ
                    ytarget=-300
                else:
                    return
            else:
                for xblock,i in enumerate(self.pazpoint[0]):#------------------------ ПОИСК Х КООРДИНАТЫ ЯЧЕЙКИ
                    if xintpos<i[0]+q.xbox:
                        xtarget=i[0]
                        break
                for yblock,i in enumerate([row[0]for row in self.pazpoint]):#-------- ПОИСК У КООРДИНАТЫ ЯЧЕЙКИ
                    if yintpos<i[1]+q.ybox:
                        ytarget=i[1]
                        break
                if self.pazmatrix[yblock][xblock]:#---------------------------------- ЕСЛИ ЯЧЕЙКА УЖЕ ЗАНЯТА
                    return
            if q.place is 2:
                self.pazmatrix[q.ymatrix][q.xmatrix]=0
            else:
                if q.place is 1:
                    q.place=2
                    self.placerecalc()
                    self.bar_recalc()
                else:
                    self.pazmatrix[q.ymatrix][q.xmatrix]=0
                    self.placerecalc()
            q.xtarget=xtarget
            q.ytarget=ytarget
            if q.place is 2:
                self.pazmatrix[yblock][xblock]=q
                q.xmatrix=xblock
                q.ymatrix=yblock
                self.winchk()
                if self.gameover:
                    q.xintpos=q.xtarget
                    q.yintpos=q.ytarget
        def winchk(self):#========================= ПРОВЕРЯЕМ СОБРАН ЛИ РИСУНОК ===================================================
            for y,i in enumerate(self.pazmatrix):
                for x,z in enumerate(i):
                    if z:
                        if not z.XNUM is x:
                            return
                        if not z.YNUM is y:
                            return
                    else:
                        return
            self.gameover=1
        def bar_recalc(self):#======================================================================================================
            if self.pazsklad:
                q=self.pazsklad.pop()
                q.place=1
                self.pazbar.append(q)
            for n,i in enumerate(self.pazbar):
                i.yintpos=self.BARYPOZ[n]
                i.xintpos=self.BARXPOZ
                i.ytarget=i.yintpos
                i.xtarget=i.xintpos
        def play(self):#===================== ОСНОВНАЯ ФУНКЦИЯ ИГРЫ ===========================================================
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
                    self.cardhit(self.movecard)
                    self.cardwalkback=1
                    self.xyspeed(self.movecard)
                    self.dropcard=0
                    self.cardnumb=-1
                    return
                self.movecard.xpos,self.movecard.ypos=MOUSEPOS()
                self.movecard.xpos-=100
                self.movecard.ypos-=100
                self.movecard.xintpos=int(self.movecard.xpos)
                self.movecard.yintpos=int(self.movecard.ypos)
        def pazcreate(self,img,num):#================== СОЗДАЁМ ФРАГМЕНТЫ =======================================================
            lis=[]
            pazsize=200
            for x in range(8):
                for y in range(5):
                    lis.append(Pazl(IMG="p{}x{}y{}".format(num,x,y),XNUM=x,YNUM=y))
                    
                    renpy.image(lis[-1].IMG,Crop((x*pazsize,y*pazsize,pazsize,pazsize),img))
            return lis
        def card_walkback(self,q):#=========== ВОЗВРАЩЕНИЕ ФРАГМЕНТА ==============================================================
            q.xpos=q.xpos+q.xspeed
            q.ypos=q.ypos+q.yspeed
            if q.steps:
                q.steps=max(0,q.steps-1)
                return
            self.cardwalkback=0
        def xyspeed(self,q):#====================== РАСЧЁТ СКОРОСТИ БОЛИДА =======================================================
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
        def placerecalc(self):#==================================================================================================
            self.pazsklad=[]
            self.paztab=[]
            self.pazbar=[]
            for i in self.pazlist:
                if i.place is 0:
                    self.pazsklad.append(i)
                elif i.place is 1:
                    self.pazbar.append(i)
                else:
                    self.paztab.append(i)
            if len(self.pazsklad)>1:
                ransh(self.pazsklad)
        def zeromatrix(self,x,y):#=========== СОЗДАНИЕ НУЛЕВОЙ МАТРИЦЫ ===========================================================
            return[[0 for _ in range(x)]for _ in range(y)]
        def __call__(self,num):#================= ЗАПУСКАЮЩАЯ МИНИ ИГРУ ФУНКЦИЯ ======================================================
            global quick_menu,pazgame
            pazgame=Pazgame()
            pazgame.pazlist=deepcopy(ALLPAZFRAG[num])
            pazgame.pazsklad=pazgame.pazlist[:]
            lastpaz=pazgame.pazsklad[-1]                                          #ПОСЛЕДНИЙ ПАЗЛ
            ransh(pazgame.pazsklad)
            pazgame.pazmatrix=self.zeromatrix(lastpaz.XNUM+1,lastpaz.YNUM+1)      #ГЕНЕРИМ НУЛЕВУЮ МАТРИЦУ
            pazgame.pazpoint=deepcopy(pazgame.pazmatrix)
            for y,i in enumerate(pazgame.pazpoint):                               #ГЕНЕРИМ МАТРИЦУ КООРДИНАТ
                for x,z in enumerate(i):
                    pazgame.pazpoint[y][x]=[x*lastpaz.xbox,y*lastpaz.ybox]
            pazgame.xmtrsize=x+1
            pazgame.ymtrsize=y+1
            for n,i in enumerate(range(pazgame.pazbarsize)):
                paz=pazgame.pazsklad.pop()
                paz.yintpos=pazgame.BARYPOZ[n]
                paz.xintpos=pazgame.BARXPOZ
                paz.ytarget=paz.yintpos
                paz.xtarget=paz.xintpos
                paz.place=1
                pazgame.pazbar.append(paz)
            quick_menu=False
            renpy.choice_for_skipping()
            renpy.call("paz_start")