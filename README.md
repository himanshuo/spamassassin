# spamassassin
spamassassin


This standalone web service allows people to use Spam Assassin for more generic content. In the OSF, this will be used
for determining if a comment is spam and determining whether a project is spam (when someone tries to make a project
public). There will be a separate PR for the code that integrates with the OSF. This service can also be used for
other purposes thus there is extra functionality that is not required for OSF integration.

<h1>How does the web service work?</h1>
This service is written in Tornado. Spam Assassin must be installed and made a daemon to make this work.
The service simply calls the bash spamc command with the appropriate parameters. The result is then parsed
to determine whether the message is spam or ham. The output of the service is simply SPAM or HAM, as appropriate.
The service basically converts the user input into an email message. The input should be json key-value pairs. All
key's that are not 'message' will become headers for this email. The 'message' key-value pair will be the content of the
email. In addition, the service allows users to send in a message to train spam assassin. It parses the message as
noted above, but additionally requires a 'is_spam' key to determine whether to teach spam assassin whether the message
is spam or not. Just as above, a process object is created. This time, however, the process object calls the
call_sa_learn.sh script which then calls the sa-learn command. This extra level of indirection is due to the fact that
sa-learn requires higher user privileges. This was the suggested solution found online (noted in code, along with a
link). A user can optionally get a full report of why whatever decision was made. A user can also optionally send in a file instead of json key-value pairs for both teaching and getting a decision.
<br/>
Internally, this service basically just pipes the user input into the spamc command attained from spamadmin. Thus, if you can tests whether spam assassin is installed correctly by running the command <br/> spamc < <filename> <br/> and the result of this is what this service is basing its return values from.

<h1>How to Install</h1>
<ol>
<li>We need to first install spam assassin. You can download it from <br/> from http://www.macupdate.com/app/mac/13526/spamassassin </li>
<li>Go to the folder you downloaded it to and unpack it</li>
<li>Open up the terminal and go to the folder you downloaded spam assassin<br/> <b>cd ~/Downloads/Mail-SpamAssassin*</b></li>
<li>Allow perl to create a Makefile for you<br/> <b>perl Makefile.PL </b></li>
<li>run the Makefile<br/><b> make</b></li>
<li>install<br/> <b>sudo make install</b></li>
<li>get spam assassin rules<br/><b> sudo sa-update --nogpg</b></li>
<br/>
<li>Go back to your home folder in your terminal<br/><b> cd ~ </b></li>
<br/>
<li>Now we need to install this standalone web service.</li>
<li>You can get it from github<br/><b> git clone https://github.com/himanshuo/spamassassin.git </b></li>
<li>Create a python virtual environment<br/> <b> mkvirtualenv --python=python3 spam3 </b></li>
<li>Go into the tornado folder via the terminal<br/><b> cd ~/spamassassin/tornado </b></li>
<li>Install requirements:<br/><b>pip install -r ~/spamassassin/requirements.txt</b></li>
<li>Run the server<br/><b> python main.py </b></li>
<br/>
<li>Almost Done! Open up a <b>new</b> terminal and start spamd (the daemonized version of spam assassin which is automatically installed
when you install spam assassin). <br/>
<b>sudo spamd</b>
</li>
<li>You're done! The standalone web service should be running now. Someone can make web requests to the localhost:8000
url with proper input and determine if their message is spam or not. This is basically what the tests do. You can run
them by running the tests in the ~/spamassassin/tornado/tests/test_spam_service.py file. <br/><b> python ~/spamassassin/tornado/tests/test_spam_service.py  </b></li>


<li>HOWEVER, you can configure spam assassin yourself to make it work better for your use case. The configuration
information section below helps with that.</li>
<li>Also, if you are having issue with your code, please look at the Issues section below. </li>
</ol>


<br/>
# Potential Issues (and Solutions):
<ol>
<li> If the result of spamc -c < <filename> is constantly 0/0 then try restarting spam assassin via <br/>
    sudo /etc/init.d/spamassassin restart
    <br/>
    spamc is the internal command that this service uses to come to a decision of whether the user input is spam or not. This service returns a 404 Internal Server Error response when this error occurs.  
    </li> 
</ol>


# Configuration Information:
<ol>
<li>Your local.cf file is a configuration file that gets appended onto regular spam assassin configurations. On a mac, this file should be at <b>/etc/mail/spamassassin/local.cf</b>. On ubuntu, it should be at /etc/spamassassin/local.cf. Edit your local.cf rules to look like the <b>spamassassin/tornado/settings/local_configs</b> file provided in this repo. <br/>  Note that
comments in this file are denoted with a # in the start of the line. Most of this file should be comments already.
More details can be found in the README file of spam assassin (~/Downloads/Mail-SpamAssassin*/README).

<li> It is useful to train spam assassin with your custom spam and/or ham files in order to make it more suitable for your purposes. In the below example, HAMFOLDER and SPAMFOLDER are your custom folders with spam and/or ham in them.</li>
    To train ham:<br/>
    sudo sa-learn --progress --ham HAMFOLDER/* <br/>
    sudo sa-learn --sync <br/>
    <br/>
    To train spam:<br/>
    sudo sa-learn --progress --spam SPAMFOLDER/* <br/>
    sudo sa-learn --sync <br/>
    <br/>
    Then, to see the contents of the spam db: (note, spamassassin basically turns messages into hashes.) <br/>
    sudo sa-learn --dump [all|magic|data]
</ol>
