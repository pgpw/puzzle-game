init -1 python:
#------------------------------------------ ИМПОРТЫ
    from math import sqrt
    from copy import deepcopy
    from random import randint as rand
    from random import choice as ranc
    from random import triangular as rant
    from random import shuffle as ransh
    from random import uniform as ranu
#------------------------------------------ КОНФИГИ
    config.keymap["button_ignore"].remove('mousedown_1')
    config.keymap["button_alternate"].remove('mouseup_3')
    config.keymap["button_alternate"].append('mousedown_1')
#------------------------------------------- СОКРАЩЕНИЯ
    PAUZA=renpy.pause
    MUSPLAY=renpy.music.play
    STOPMUS=renpy.music.stop
    SNDPLAY=renpy.play
    MOUSEPOS=renpy.get_mouse_pos
#-------------------------------------------- РАЗРАБОТКА
    minigame_skip=0
#-------------------------------------------- ПЕРЕМЕННЫЕ
    pazgame=Pazgame()
#-------------------------------------------- КОНСТАНТЫ
    ALLPAZFRAG=[]
    for n,i in enumerate(renpy.list_files()):
        if i.startswith("paz7/img/"):
            ALLPAZFRAG.append(pazgame.pazcreate(i,n))