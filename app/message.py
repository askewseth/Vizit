#Module to hold special messages to be displayed throughout the site.
# The purpose is to have easy access when new messages are to be added
# and when old messages are to be edited.  This also prevents from having
# to create a separate html template for each page when sometimes different
# messages are displayed on the same page.

from flask import Markup

def returnWelcome():
    message = Markup('<p style=\"padding-left:30px; padding-right:30px\">Welcome to the Vizit statistical web site.  The purpose of this site is to provide users a quick reference to statistical data calculated '
    + 'from a set of numbers.  Enter any given comma separated values into the text box above to give it a try.  You can also '
    + '<a href=\"/register\">create an account</a> for additional features such as graph plots and query history.</p>')
    return message

def returnLoginError():
    message = Markup('<label style=\"color:red; font-size:16pt\">ERROR:</label><p>The username or password you entered above is incorrect.  Please check '
    + 'your input for errors and try again.  If you do not have an account, you can <a href=\"/register\">create an account</a> for additional '
    + 'features such as graph plots and query history.</p>')
    return message


def returnNewAccountError():
    return None


def returnDisclaimer():
    message = Markup('<p>Thank you for your interest in the Vizit website.  This site was created as a Software Engineering project for students '
    + 'attending the University of North Carolina Greensboro.  As students, the creators are non-profit and are not affiliated with any form of data mining entity. '
    + 'The Vizit website takes great pride in security issues and this site will not collect any personal information from its users. The email address you provide will '
    + 'only be used for identification purposes and in the event you need to request your password should it become lost. Vizit will not share your email or password with ANYONE!! '
    + 'Please take a moment to sign up for additional site services by providing the requested credentials.  Please remember to check the agree box to the terms before submitting.</p>')
    return message

def returnLoggedOutMenuBar():
    message = Markup('<div class=\"loginbar\"><form action=\"/login\" method="post"><span><label class=\"loginFormat\">Enter Email:</label>'
    + '<input class=\"loginFields\" type=\"text\" name=\"email\"><label class=\"loginFormat\">Password:</label><input class=\"loginFields\" type=\"password\" name=\"password\">'
    + '<button class=\"loginButton\" type=\"submit\">LOGIN</button></span></form><form action=\"/register\" method=\"get\">'
    + '<button class=\"newAccountButton\" type=\"submit\">Create Account</button></form></div>')
    return message

def returnLoggedInMenuBar():
    message = Markup('<div class="linksbar"><ul id="menu"><li style="margin-right:100px"><a href="/">Homepage</a><link><li style="margin-right:100px"><a href="/plot_data">Plots/Graphs</a><link><li style="margin-right:100px"><a href="/history">History</a><link>'
    + '<li><a href="/logout">Log Out</a><link></ul></div>')
    return message

def returnNewAccountSuccessful():
    message = Markup('<label style="font-size:16pt; color:blue">SUCCESS:&nbsp;New Account Created</label><p>Thank you for taking the time to create your account with Vizit.&nbsp; As '
    + 'a member, you now have additional options from which to choose. The creators of this site hope these new features will enhance your Vizit experience.</p>')
    return message

def returnNewAccountFailure():
    message = Markup('<label style="color:red; font-size:16pt">ERROR: New Account Rejected</label><p>A member of the site has already registered with the email address entered.'
                     + 'If you have already created an account with us before, then please try to log into your account with the same email and the password you used when the '
                     + 'account was first created.  If you do not remember your password, then you must currently create a new account and use a different '
                     + 'email.&nbsp; Vizit is deeply sorry for any inconvience this may have caused.</p>')
    return message

def returnWelcomeLoggedIn():
    message = Markup('<p style=\"padding-left:30px; padding-right:30px\">Welcome back to the Vizit statistical web site.  We hope you enjoy your stay.  The purpose of this site is to '
    + 'provide users a quick reference to statistical data calculated '
    + 'from a set of numbers.  Enter any given comma separated values into the text box above to give it a try or click one of the bottons at the top for more options.')
    return message
