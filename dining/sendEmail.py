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
        Greeting = 'Hello, \n\n' #We have a good news for you!\n\n'
        body1 = ''
        body2 = ''

        ## iterate through the list of favorites available today
        #print favorites[netid]
        for tup in favorites[netid]:
            (item, dininghall, when, exact) = tup
            if (exact == None):
                body1 += item +" is available at "+dininghall+" for "+when+". \n"
            else:
                body2 += "You like "+exact+" so we thought you might enjoy "+item+" which is available at "+dininghall+" for "+when+". \n"
        #    print item
        #    print dininghall
        #    print when

        if (body1 != ''):
            texttosend = Greeting+'We have a good news for you!\n\n'+body1+'\n'+body2+'\nBest,\nTiger Bites'
        else:
            texttosend = Greeting+body2+'\nBest,\nTiger Bites'
        #body += '\nBest,\nTiger Bites'

        ## send!
        message.set_text(texttosend)
        message.set_from('Tiger Bites <princetontigerbites@gmail.com>')
        status, msg = sg.send(message)
