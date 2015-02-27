from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response


#using appropriate file parser
from rest_framework.parsers import FileUploadParser
#for calling spamc
from subprocess import *
import shlex

# Create your views here.





#handle result
def handle_result(result):
    result_val = eval(result[0].strip())
    print result_val
    if result_val<1:
        return Response("OK", status=status.HTTP_200_OK)
    else:
        return Response("SPAM", status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@parser_classes((FileUploadParser,))
def spam_or_ham(request):
    """
    Determine whether input email (text file) is spam or not. Uses SpamAssassin.
    """

    #memory version (small files aka less than 2.5 mb which is actually huge for email.)
    try:

        #get email
        file =  request.FILES['file'] #this is problematic if file is too big.

        email = file.read()

        #setup command
        command = "spamc -c"
        args = shlex.split(command)

        #send command and get result
        proc = Popen(args, stdin=PIPE, stdout=PIPE)
        result= proc.communicate(email)

        return handle_result(result)

    except Exception as e:
        print e
        return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)




    #external file version

    """
    try:
        request.FILES['file']
    except Exception as e:
        print e

    """

    #email = request.FILES['email']


    #return Response({'received data': str(request.FILES['file'])})

