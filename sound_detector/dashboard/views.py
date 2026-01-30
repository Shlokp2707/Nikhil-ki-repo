from django.shortcuts import render,redirect
from . import model
from langchain_core.messages import HumanMessage
from .models import IncidentHistory
from . import alertllm
llm =alertllm.LLM()
from accounts.models import Myuser
# Create your views here.
def udashboard(request):
    user =Myuser.objects.filter(u_id=request.session.get("user_id")).first()
    if not user:
        return redirect("login") 
    li =[]
  
    context ={'name':user.first_name}
    for i in IncidentHistory.objects.filter(user=user):
           li.append(HumanMessage(content = f"confidence = {i[2]}, class = {i[3]}, time = {i[4]}, date = {i[5]}"))
    if request.method=='POST':
        current_situaton =model.predict_sound(2)
        print(current_situaton)

        result =llm.callLLM(user.u_id,li,current_situaton,user.email)
        print()
        print("hello world", result)
        print()
    return render(request,'dashboard.html',context)
