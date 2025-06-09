import os
import re
from dhooks import Webhook

webhook_map = {
    "1": "https://discord.com/api/webhooks/1380799326837538846/lS99Z88dLAoyktKIZUhqRUoZK14dIO-qxr35K4xrM81jYbtlwOl_9-YkkSnVDlJBgplW",
    "2": "https://discord.com/api/webhooks/1381629785758892302/l1IFjvKN2GMmr38ifExdJdWKOQ2ApblmslYsCxgT15EV-VIF-ep7TO06Ac81owZRT10c",
    '3': "https://discord.com/api/webhooks/1381675601521541180/ArN2aQzlI3Im8oSr0eYRBEuQ-KtUI8t-rAIpkCQ4xHys7Z4hr9D4gkn23xrkHWw-DkZ1",
    '4': "https://discord.com/api/webhooks/1380829000175325324/p1Zgdsj9c93ZqxXRgNazTx_RahWesTep_0j_DuGRxBGqUrTmsPXmUQZ0jIwzu_4x-C_9",
    '5': 'https://discord.com/api/webhooks/1381675605833285743/0SS3Di02s8lgThWi6KNW1IecsaAGrwmvwpM7OY44GVbHfMT-JocQXNzdAGlxdWi74UAt',
    '6': "https://discord.com/api/webhooks/1380734207806013461/QgOSRB5ON7wDOi1zj7Mu_IcSGS23pk7ANABoHBBtcACuwyBGPmM9rBsHMA78tlSCLwCS",
    '7': 'https://discord.com/api/webhooks/1381675297954332825/8yIl1wolbf5dh2UERKSJEhxM3Gpkfp4dWgoN9rDx9L1VT8h5WCJujVbD8IwamJNQg6Hk',
    '8': 'https://discord.com/api/webhooks/1381675286030192681/WAiEHPFLmMFobdeUlKU_8wsSikYMU_PvUrkLRhks3-znwAmmoxYDJYoh79bWZ9sl_q0m',
}

bot_path = os.getcwd()  # Gets the current working directory path
match = re.search(r'bot (\d+)', bot_path, re.IGNORECASE)

if match:
    bot_number = (match.group(1))
    DC_webhook = webhook_map.get(bot_number)

else:

    DC_webhook = 'https://discord.com/api/webhooks/1381683293291937943/0_UP8fE31Xs8u7dafpEljIfR_T_JpwjAOI4ol_xk1-RE0EUKH2WVaG7GJzvLprJoPyGF'
    hook = Webhook(DC_webhook)
    hook.send(f"<@&1380790894248202282> gg,unable to find hook for some bot(s)")



GTDELAY = 3 #delay for go_to functions, for mini pc, use 5
MIN_HP = 50
MIN_MP = 10
BUTTON_MP,BUTTON_HP = 'j','h'
