import sendgrid


def sendEmail(favorites):

    ##key: netid
    ##values: list of tuples(item, dinighall, when)


    sg = sendgrid.SendGridClient('tigerbites', 'princetoncos333')

    for netid in favorites:
       # print netid
        message = sendgrid.Mail()
        useremail = '<'+netid+'@princeton.edu>'
        message.add_to(useremail)
        message.set_subject('Daily Notification from TigerBites')

        ## body of the email
        #Greeting = 'Hello, \n\n' #We have a good news for you!\n\n'
        Greeting = '<html><body><font face = "Lucida Sans Unicode"><h1>Hello!</h1>'
        perfect = '<p>We have good news!</p>'
        suggest1 = '<p>AND why not try something new?</p>'
        suggest2 = "<p>We couldn't find your favorites today,<br>BUT why not try something new?</p>"
        body1 = ''
        body2 = ''
        signoff = '<br><p align = "right">Best,&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<br>Tiger Bites!&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;</p><br><p><center><font size="1">To see more dining options, or make suggestions, please visit <a href="http://tigerbites.org">tigerbites.org</a><br>To end email service, visit <a href="www.tigerbites.org/favorites>tigerbites.org/favorites</a> and remove unwanted favorited items.</p></font></body></html>'
        finishlist = "</ul>"
        ## iterate through the list of favorites available today
        #print favorites[netid]
        for tup in favorites[netid]:
            (item, dininghall, when, exact) = tup
            if (exact == None):
                if (body1 == ''):
                    body1 += '<ul>'
                body1 += "<li><big>"+item +"</big> is available at <big>"+dininghall+"</big> for <big>"+when+"</big>. </li>"
            else:
                if (body2 == ''):
                    body2 += '<ul>'
                body2 += "<li>You like <big>"+exact+"</big> so we thought you might enjoy <big>"+item+"</big> which is available at <big>"+dininghall+"</big> for <big>"+when+"</big>. </li>"


        if (body1 != ''):
            if (body2 != ''):
                texttosend = str(Greeting)+str(perfect)+str(body1.encode('utf-8'))+str(finishlist)+str(suggest1)+str(body2.encode('utf-8'))+str(finishlist)+str(signoff)
            else:
                texttosend = str(Greeting)+str(perfect)+str(body1.encode('utf-8'))+str(finishlist)+str(signoff)
        else:
            texttosend = str(Greeting)+str(suggest2)+str(body2.encode('utf-8'))+str(finishlist)+str(signoff)

        ## send!
        message.set_html(texttosend)
        message.set_from('Tiger Bites <princetontigerbites@gmail.com>')
        if (netid == 'yktwo'):
            status, msg = sg.send(message)
