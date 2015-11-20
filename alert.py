import smtplib

server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.ehlo()
server.starttls()
server.login('scottdpost@gmail.com', 'Scottyp123')
server.sendmail( 'Scott Post', '8472247292@mms.att.net', 'You should purchase TASR' )
server.sendmail( 'Abhi Desai', '7325475739@vtext.com', 'You should purchase TASR' )