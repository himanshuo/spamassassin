#!/bin/bash


#parallel ::: "spamc -c < large_spam.txt" "spamc -c < sample-nonspam.txt" "spamc -c < non_spam_with_no_email_headers.txt" 
#curl http://localhost:8000/?id=1&email=as

#parallel curl ::: http://localhost:8000/?id=1&email=buybuybuy http://localhost:8000?id=2 http://localhost:8000/?id=3 http://localhost:8000/?id=4 http://localhost:8000/?id=5

parallel curl ::: http://localhost:8000?email=buybuybuybuybuybuybuybuyb http://localhost:8000?id=2

