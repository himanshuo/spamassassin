#!/bin/bash


#parallel ::: "spamc -c < large_spam.txt" "spamc -c < sample-nonspam.txt" "spamc -c < non_spam_with_no_email_headers.txt" 
#curl http://localhost:8000/?id=1&email=as

#parallel curl ::: http://localhost:8000/?id=1&email=buybuybuy http://localhost:8000?id=2 http://localhost:8000/?id=3 http://localhost:8000/?id=4 http://localhost:8000/?id=5

#parallel curl ::: http://localhost:8000?email=buybuybuybuybuybuybuybuyb http://localhost:8000?id=2

parallel --joblog ./log  -q ::: 'curl http://localhost:8000 -d "afsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notafsdf i like pie and apples and cherries and what not and what else cna i write that looks like spam maybe some references to nigerian princes and what notv"' 'curl http://localhost:8000 -d love' 'curl http://localhost:8000 -d r' 'curl http://localhost:8000 -d 1'

