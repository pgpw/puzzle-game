screen key_off():#========================== ОТКЛЮЧЕНИЕ КЛАВИШ =================================
    key"rollback"action NullAction()
    key"viewport_wheelup"action NullAction()
    key"viewport_wheeldown"action NullAction()
    key"viewport_up"action NullAction()
    key"viewport_down"action NullAction()
    key"hide_windows"action NullAction()
screen pazpaz():#@@@@@@@@@@@@@@@@@@@@@@@@@@@ ОСНОВНОЙ СКРИН ИГРЫ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    use key_off
    if not pazgame.gameover:
        timer.025 repeat 1 action Function(pazgame.play)
        if not pazgame.cardwalkback and pazgame.cardnumb<0:
                for n,i in enumerate(pazgame.pazbar):
                    imagebutton idle i.IMG pos(i.xintpos,i.yintpos)alternate[SetField(pazgame,"movecard",i),SetField(pazgame,"cardnumb",n)]action SetField(pazgame,"dropcard",1)
                for n,i in enumerate(pazgame.paztab):
                    imagebutton idle i.IMG pos(i.xintpos,i.yintpos)alternate[SetField(pazgame,"movecard",i),SetField(pazgame,"cardnumb",n)]action SetField(pazgame,"dropcard",1)
        else:
            for n,i in enumerate(pazgame.pazbar):
                add i.IMG pos(i.xintpos,i.yintpos)
            for n,i in enumerate(pazgame.paztab):
                add i.IMG pos(i.xintpos,i.yintpos)
            if pazgame.cardnumb>-1:
                imagebutton idle"paz7/ui/e.w"action[SetField(pazgame,"dropcard",1),SetField(pazgame,"hovercard",-1)]
                add pazgame.movecard.IMG pos(pazgame.movecard.xintpos,pazgame.movecard.yintpos)
    else:
        text"win"align(.5,.5)
    use paztest
screen paztest():#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    vbox align(.5,.5):
        if pazgame.pazbar:
            text str (pazgame.pazbar[0].xintpos)
            text str (pazgame.pazbar[0].yintpos)