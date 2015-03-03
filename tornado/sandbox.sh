#!/bin/bash


#parallel ::: "spamc -c < large_spam.txt" "spamc -c < sample-nonspam.txt" "spamc -c < non_spam_with_no_email_headers.txt" 


parallel curl ::: http://localhost:8000/?id=1 http://localhost:8000/?id=2 http://localhost:8000/?id=3 http://localhost:8000/?id=4 http://localhost:8000/?id=5



