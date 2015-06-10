# spamassassin
spamassassin



This service is written in Tornado. Spam Assassin must be installed and made a daemon to make this work. The service simply calls the bash spamc command with the appropriate parameters. The result is then parsed to determine whether the message is spam or ham. The output of the service is simply SPAM or HAM, as appropriate.

The service basically converts the user input into an email message. The input should be json key-value pairs. All key's that are not 'message' will become headers for this email. The 'message' key-value pair will be the content of the email.

In addition, the service allows users to send in a message to train spam assassin. It parses the message as noted above, but additionally requires a 'is_spam' key to determine whether to teach spam assassin whether the message is spam or not. Just as above, a process object is created. This time, however, the process object calls the call_sa_learn.sh script which then calls the sa-learn command. This extra level of indirection is due to the fact that sa-learn requires higher user privileges. This was the suggested solution found online (noted in code, along with a link).

A user can optionally get a full report of why whatever decision was made. A user can also optionally send in a file instead of json key-value pairs for both teaching and


#Issues:
1) if the result of spamc -c < <filename> is constantly 0/0 then try restarting spam assassin via
    sudo /etc/init.d/spamassassin restart


# Configuration Information:
1) Edit /etc/spamassassin/local.cf (or wherever your configurations are) and make it look like tornado/settings/local_configs
2) Will have to train spam assassin.
    To train (note that all_ham, all_spam folders are provided in repo):
    sudo sa-learn --progress --ham HAMFOLDER/*
    sudo sa-learn --sync
    <br/>
    Then, to see the contents of the spam db: (note, spamassassin basically turns messages into hashes.)
    sudo sa-learn --dump [all|magic|data]

