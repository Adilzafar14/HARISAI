def classify_gesture(landmarks, hand_label):

    # Fist = Emergency SOS
    fist_tips = [8, 12, 16, 20]
    fist_mcp  = [5,  9, 13, 17]
    if all(landmarks[t].y > landmarks[m].y 
           for t, m in zip(fist_tips, fist_mcp)):
        return 'SOS', 0.93

    # One finger = Navigation
    index_up  = landmarks[8].y  < landmarks[6].y
    middle_dn = landmarks[12].y > landmarks[10].y
    ring_dn   = landmarks[16].y > landmarks[14].y
    pinky_dn  = landmarks[20].y > landmarks[18].y
    if index_up and middle_dn and ring_dn and pinky_dn:
        return 'NAVIGATE', 0.89

    # V sign = Lost Pilgrim
    middle_up = landmarks[12].y < landmarks[10].y
    if index_up and middle_up and ring_dn and pinky_dn:
        return 'LOST', 0.87

    # Open hand = Help
    count = 0
    if hand_label == 'Right':
        if landmarks[4].x < landmarks[3].x:
            count += 1
    else:
        if landmarks[4].x > landmarks[3].x:
            count += 1

    tips = [8, 12, 16, 20]
    base = [5,  9, 13, 17]
    for t, b in zip(tips, base):
        if landmarks[t].y < landmarks[b].y:
            count += 1

    if count >= 4:
        return 'HELP', 0.91

    return 'NONE', 0.0


GESTURE_ACTIONS = {
    'HELP':     'Help request — Guide dispatched',
    'NAVIGATE': 'Navigation — Route activated',
    'LOST':     'Lost pilgrim — Group finder ON',
    'SOS':      'EMERGENCY — All units alerted!',
    'NONE':     'No gesture detected',
}


def get_action(gesture):
    return GESTURE_ACTIONS.get(gesture, 'Unknown')