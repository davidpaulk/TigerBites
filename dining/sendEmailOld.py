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
        body = 'Hello, \n\nThe following items are available today!\n\n'
 
        ## iterate through the list of favorites available today
        #print favorites[netid]
        for tup in favorites[netid]:
            (item, dininghall, when) = tup
            body += item +" is available at "+dininghall+" for "+when+". \n"
        #    print item
        #    print dininghall
        #    print when

        body += '\nBest,\nTiger Bites'

        ## send!
        message.set_text(body)
        message.set_from('Tiger Bites <princetontigerbites@gmail.com>')
        status, msg = sg.send(message)
