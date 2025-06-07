def lef():
    pt1 = 107
    pt2 = 130
    pt3 = 152
    marker_pos = find_marker_location()
    hp = pot.get_hp()
    print(f"HP: {hp:.2f}%")
    mp = pot.get_mp()
    print(f"MP: {mp:.2f}%")
    chance = random.random()
    #use hp pot
    if hp < POT_HP and chance < 0.15:
        pdi.press(BUTTON_HP)
    elif hp < MIN_HP:
        pdi.press(BUTTON_HP)
    # use mp pot
    if mp < POT_MP and chance < 0.15:
        pdi.press(BUTTON_MP)
    elif mp < MIN_MP:
        pdi.press(BUTTON_MP)
        set_paused(2)

    if auto == False:
        time.sleep(1)
        print("Auto = False")
    elif marker_pos[1] < pt1+2:  # 1st platform
        if chance > 0.95 and marker_pos[0] > 80 :
            pdi.press('left')
            pdi.press('space')
            pdi.press('space')
            time.sleep(0.3 + random.random() * 0.2)
            pdi.press('right')
            pdi.press('x')
        elif chance > 0.8 and marker_pos[0] < 93:
            pdi.keyDown('right')
            pdi.press('x')
            time.sleep(0.4 + random.random())
            pdi.keyUp('right')
            time.sleep(chance * 0.2)
            pdi.press('left')
            pdi.press('x')
        else:
            pdi.press('left')
            pdi.press('x')
            time.sleep(0.3 + random.random() * 0.2)
            pdi.press('right')
            pdi.press('x')
        time.sleep(0.3+ random.random()*0.2)
        pdi.keyDown('down')
        pdi.press('space')
        time.sleep(0.1 + random.random()*0.1)
        pdi.keyUp('down')
        times = 0

    elif marker_pos[1] < pt2-2:  # ladder
        if marker_pos[0] > 80:
            pdi.keyDown('left')
            pdi.press('space')
            pdi.keyUp('left')
        else:
            pdi.keyDown('right')
            pdi.press('space')
            pdi.keyUp('right')

    elif marker_pos[1] < pt2+2:  # 2nd platform
        pdi.press('left')
        pdi.press('x')
        time.sleep(0.3+ random.random()*0.3)
        pdi.press('right')
        pdi.press('x')
        time.sleep(0.3+ random.random()*0.2)
        pdi.keyDown('down')
        pdi.press('space')
        time.sleep(0.1 + random.random()*0.1)
        pdi.keyUp('down')

    elif marker_pos[1] < pt3-2:  # ladder
        if marker_pos[0] > 80:
            pdi.keyDown('left')
            pdi.press('space')
            pdi.keyUp('left')
        else:
            pdi.keyDown('right')
            pdi.press('space')
            pdi.keyUp('right')

    elif marker_pos[1] < pt3+2:  # 3rd platform
        if marker_pos[0] == 98 or marker_pos[0] == 97:
            pdi.press('up')
            return
        elif chance > 0.95 and marker_pos[0] > 85:
            pdi.press('left')
            pdi.press('space')
            pdi.press('space')
            time.sleep(0.3)
            pdi.press('right')
            pdi.press('x')
            time.sleep(0.3)
        elif chance > 0.95 and marker_pos[0] < 85:
            pdi.press('right')
            pdi.press('space')
            pdi.press('space')
            time.sleep(0.3)
            pdi.press('left')
            pdi.press('x')
        else:
            pdi.press('left')
            pdi.press('x')
            time.sleep(0.3+ random.random()*0.2)
            pdi.press('right')
            pdi.press('x')
            time.sleep(0.3)
        if marker_pos[0] == 98 or marker_pos[0] == 97:
            pdi.press('up')

        else:
            go_to(97)