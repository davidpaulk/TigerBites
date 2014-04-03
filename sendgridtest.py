import sendgrid

sg = sendgrid.SendGridClient('tigerbites', 'INSERT_PASSWORD_HERE')

message = sendgrid.Mail()
message.add_to('David <dpaulk@princeton.edu>')
message.set_subject('Title goes here')
message.set_text('Hello David!')
message.set_from('Tiger Bites <princetontigerbites@gmail.com>')
status, msg = sg.send(message)