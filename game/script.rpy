define e = Character('Эйлин', color="#c8ffc8")
label start:
    pass
label pazlabel:
    menu:
        e"ВЫБЕРЕТЕ ПАЗЛ"
        "первый пазл":
            $pazgame(1)
        "второй пазл":
            $pazgame(2)
        "третий пазл с рамкой":
            $pazgame(3)
    jump pazlabel
    return
