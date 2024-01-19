from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import RunCode
import os
import json
from rest_framework.parsers import MultiPartParser , FormParser

# Create your views here.
class CodeExecutor(APIView):
    
    parser_classes = [MultiPartParser , FormParser ,] 

    def get(self , request , *args):
        
        return Response({"message" : "Send a post request with the python code"} , status=status.HTTP_200_OK)
    
    
    def post(self , request , *args) :
        
        try:
            
            # data = request.body.decode('utf-8')
            data = request.POST.get('code', None)
            inp = request.POST.get('inp', None)
            print(data)
            print(inp)
                        
            if data is None :
                return ValueError({"message" : "No code found"})

            with open("./api/python_runner/temp.py","w+",buffering=100) as temp:
                temp.write(data)
            
            with open("./api/python_runner/tempi.txt","w+",buffering=100) as temp:
                temp.write(inp)
                
            runcode = RunCode()
            
            output = runcode.runPythonCode()
            
            response = {"output" : output}
  
            os.remove("./api/python_runner/temp.py")
            os.remove("./api/python_runner/tempi.txt")
                
            return Response(response , status=status.HTTP_200_OK)
                            
        except Exception as e:
            response = {"message" : str(e)}
            return Response(response , status=status.HTTP_500_INTERNAL_SERVER_ERROR)