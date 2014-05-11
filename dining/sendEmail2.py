import sendgrid
import time, datetime

def sendEmail(favorites):

    sg = sendgrid.SendGridClient('tigerbites', 'princetoncos333')

    for netid in favorites:

        message = sendgrid.Mail()
        useremail = '<'+netid+'@princeton.edu>'
        message.add_to(useremail)

        ## body of the email
        Greeting = '<html><style> .one{border-style:outset;border-color:orange;} </style><body class = "one"><center><a href="http://tigerbites.org"><img src = "http://www.princeton.edu/~yktwo/logo13.png" width="200"></a></center><font face = "Lucida Sans Unicode"><hr>'
        perfect = ''
        mealtime = ''
        suggest1 = '<p>AND why not try something new?</p>'
        suggest2 = "<p>We couldn't find your favorites today,<br>BUT why not try something new?</p>"
        body1 = ''
        body2 = ''
        signoff = '<br><hr><p><i><center> To see more dining options, please visit <a href="http://tigerbites.org">tigerbites.org</a><br>To end email service, visit <a href="www.tigerbites.org/favorites">tigerbites.org/favorites</a> and remove unwanted favorited items.</i></p></font></body></html>'
        finishlist = "</ul></ul>"

        ## iterate through the list of favorites available today         
        for dininghall in favorites[netid].keys():
            if (dininghall == 'ROCKY'):
                dhall1 = 'Rocky / Mathey'
                dhall = '<img src = "http://www.princeton.edu/~yktwo/rocky" height = "50"><img src = "http://www.princeton.edu/~yktwo/mathey" height = "50"><br>[ Rocky / Mathey ]'
            elif (dininghall == 'WILSON'):
                dhall = '<img src = "http://www.princeton.edu/~yktwo/wilson" height = "50"><img src = "http://www.princeton.edu/~yktwo/butler" height = "50"><br>[ Wilson / Butler ]'

                dhall1 = 'Wilson / Butler'
            elif (dininghall == 'FORBES'):
                dhall = '<img src = "http://www.princeton.edu/~yktwo/forbes" height = "50"><br>[ Forbes ]'
                dhall1 = 'Forbes'
            elif (dininghall == 'GRADCOLLEGE'):
                dhall = '<img src = "https://web.math.princeton.edu/~kfelker/images/Princeton-Logo.jpg" height = "50"><br>[ Graduate Collge ]'
                dhall1 = 'Graduate College'
            elif (dininghall == 'WHITMAN'):
                dhall = '<img src = "http://www.princeton.edu/~yktwo/whitman" height = "50"><br>[ Whitman ]'
                dhall1 = 'Whitman'
            elif (dininghall == 'CJL'):
                dhall = '<img src = "http://www.saveachildsheart.org/sip_storage/FILES/1/3191.jpg" height = "50"><br>[ CJL ]'
                dhall1 = 'CJL'
            else:
                dhall = dininghall
            cnt = 0
            if (body1 != ''):
                body1 += '<hr width = "50%">'
            for tup in favorites[netid][dininghall]:
                (item, when, exact) = tup
                if (mealtime == ''):
                    mealtime = when
                if (exact == None):

                    if (cnt == 0):
                        body1 += "<p><big><center>"+dhall+'</big></p><p><center>'+item
                    else:
                        body1 += '<br>'+item
                    cnt+=1
                else:
                    if (body2 == ''):
                        body2 += '<ul>'

                    body2 += "<li>You like <big>"+exact+"</big> so we thought you might enjoy <big>"+item+"</big> which is available at <big>"+dhall1+"</big>.</li> "
            if cnt > 0:
                body1+="</center></p>"
           

        if (body1 != ''):
            body1 +="</p>"
            if datetime.datetime.now().isoweekday() == 7:
                if mealtime == "LUNCH":
                    perfect = "<p><center><i>"+time.strftime("%A, %b %d")+"</i><br>Your favorite(s) served for BRUNCH:</center></p>"
                    mealtime = "BRUNCH"
            elif datetime.datetime.now().isoweekday() == 6:
                if mealtime == "LUNCH":
                    perfect = "<p><center><i>"+time.strftime("%A, %b %d")+"</i><br>Your favorite(s) served for BRUNCH:</center></p>"
                    mealtime = "BRUNCH"
            else:
                perfect = "<p><center><i>"+time.strftime("%A, %b %d")+"</i><br>Your favorite(s) served for "+mealtime+":</center></p>"
            if (body2 != ''):
                texttosend = str(Greeting)+str(perfect)+str(body1.encode('utf-8'))+str(finishlist)+str(suggest1)+str(body2.encode('utf-8'))+str(finishlist)+str(signoff)
            else:
                texttosend = str(Greeting)+str(perfect)+str(body1.encode('utf-8'))+str(finishlist)+str(signoff)
        else:
            texttosend = str(Greeting)+str(suggest2)+str(body2.encode('utf-8'))+str(finishlist)+str(signoff)

        ## send!
        message.set_subject('TigerBites Notification for '+mealtime)
        message.set_html(texttosend)
        message.set_from('Tiger Bites <princetontigerbites@gmail.com>')
#        if (netid == 'yktwo'):
        status, msg = sg.send(message)

