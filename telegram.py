import requests

TGID='5081261439'
TGTOKEN='5079203145:AAH3agixAvHmbCnL9EPntNSHGSqr1obxo24'

def SendToMyTelegram(text):
    url = 'https://api.telegram.org/bot5079203145:AAH3agixAvHmbCnL9EPntNSHGSqr1obxo24/sendMessage'
    parameters={'chat_id':TGID, 'text':text}
    requests.get(url, params=parameters)

def SendToMyTelegramASMRobot(text):
    url = 'https://api.telegram.org/bot5282466435:AAGH2yihX3ZAG-Wo0ou2JdkyIl6DGea5xiE/sendMessage'
    parameters={'chat_id':TGID, 'text':text}
    requests.get(url, params=parameters)
    
def SendToMyTGChannel(text):
    url = 'https://api.telegram.org/bot5079203145:AAH3agixAvHmbCnL9EPntNSHGSqr1obxo24/sendMessage'
    parameters={'chat_id':-1001768296044, 'text':text}
    requests.post(url, params=parameters)

def SendToMyTGChannelFile(file):
    url = 'https://api.telegram.org/bot5079203145:AAH3agixAvHmbCnL9EPntNSHGSqr1obxo24/sendDocument'
    parameters={'chat_id':-1001768296044}
    requests.post(url, params=parameters, files={'document': open(file,'rb')})

if __name__=='__main__':
    text = '''
What: ASMEmailTG<br> When: February 18, 2022 at 05:44PM<br> Extra Data: You have unread notifications in ASM <https://recruitee-assets.s3.eu-central-1.amazonaws.com/system-emails/assets/recruitee-0e2cdc4c090a0df5a68f0568e3b68cab.png> 2 notifications You have some unread notifications in ASM. <https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/168435/thumb_avatar_1uhoybfpdhwv.png> ________________________________ <https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/162306/thumb_avatar_e1lofn1lmuh1.png> Kenneth Fung added a team note to candidate Chan Yuen Chung <https://app.recruitee.com/#/dashboard/overview?candidate=33498831&company=38422> . ________________________________ <https://recruitee-main.s3.eu-central-1.amazonaws.com/admins/162306/thumb_avatar_e1lofn1lmuh1.png> Kenneth Fung added a team note to candidate Chan Yuen Chung <https://app.recruitee.com/#/dashboard/overview?candidate=33498831&company=38422> . Go to notifications <https://app.recruitee.com/#notifications?company_id=38422> , , ,
    '''
    #SendToMyTGChannel(text)
    SendToMyTGChannelFile('1.pdf')