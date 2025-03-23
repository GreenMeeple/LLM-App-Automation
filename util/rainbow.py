def try_click_send_button(message_box, appId):

    if appId == 'com.larus.wolf' or appId == 'ai.socialapps.speakmaster':
        s = message_box.sibling(resourceIdMatches=".*[s|S]en[t|d].*")
        if s:
            s[-1].click()

    if appId == 'ai.character.app':
        for s in message_box.sibling(clickable=True):
            s.click()

    if appId == 'com.codeway.chatapp' or appId == 'com.hiwaifu.app' or appId == 'com.codespaceapps.aichat':
        s = message_box.sibling(clickable=True, resourceIdMatches="")
        if s:
            s[-1].click()

    if appId == 'com.weaver.app.prod' or appId == 'com.qianfan.aihomework':
        for s in message_box.sibling(resourceIdMatches=".*[s|S]en[t|d].*"):
            s.click()

    else: 
        for s in message_box.child(resourceIdMatches=".*[s|S]en[t|d].*"):
            s.click()

    # possible ways to locate a send button:

    # # Works on: 
    # for s in message_box.child(clickable=True):
    #     s.click()

    # # Works on: 
    # s = d(descriptionMatches = ".*[s|S]en[t|d].*")
    # if s:
    #     s.click()

    # # Works on: 
    # for s in message_box.child(resourceIdMatches=".*[s|S]en[t|d].*"):
    #     s.click()