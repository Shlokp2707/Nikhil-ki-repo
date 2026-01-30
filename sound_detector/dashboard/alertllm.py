 # library and api import
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
# load_dotenv()
hfSecretKey = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
from .Tools import sendMail





# input of model in form of :-
# HumanMessage(["confidenceLevel", "predictionClass", "timeOfIncident", "dateOfIncident"]),
class LLM:

    # system message creation
    system_message = '''You are “The Smart Home Ear” incident management system.

    Input:
    - Historical incidents: incidents = [HumanMessage([confidenceLevel, predictionClass, timeOfIncident, dateOfIncident])]
    - A separate current HumanMessage with the same structure (not part of history).

    Task:
    Determine if the current incident is dangerous using:
    - confidenceLevel and predictionClass
    - timeOfIncident (night or unusual hours) and dateOfIncident
    - patterns or escalation in historical incidents, primarly focus on current incidents

    Danger includes:
    - High-confidence dangerous sounds(e.g., scream,gun shot, glass_break, gunshot, a baby crying, fire alarms)
    - Repeated similar dangerous sounds in history or present
    - Dangerous sounds at night or unusual times
    - Increasing confidence or frequency

    Rules:
    - If the incident is dangerous, call the `SendMail` tool exactly once.
    - If the incident is not danger'''

    # message template
    message_template = ChatPromptTemplate([
        ("system", "{system_message}"),
        MessagesPlaceholder(variable_name = "incidents_history"),
        ("human", "{current_situation}")
    ])
    # model creation
    llm = HuggingFaceEndpoint(
        model = "zai-org/GLM-4.7",
        # model ="mistralai/Mistral-7B-Instruct-v0.3",
        task = 'text-generation',
        provider = "novita",
        huggingfacehub_api_token = hfSecretKey)
    alarmModel = ChatHuggingFace(llm = llm).bind_tools([sendMail])
    # chain to connect message and model
    chain = message_template | alarmModel

    # used to call llm for sending mail
    def callLLM(self, uid, incidents_history, current_situation, user_gmail):
        print("calling the llm")
        self.responce = self.chain.invoke({"system_message" : self.system_message, "incidents_history" : incidents_history, "current_situation" : current_situation}).tool_calls

        print()
        print("message is : ")
        print(self.system_message, incidents_history, current_situation)
        print()
        print("response from llm", self.responce)
        print()

        if self.responce:
            print("response is commin ")
            # for single_message in current_situation:
            #     p
                # single_var = single_message.content.split(", ")
                
                # db.insertIntoIncidentTB(uid, float(single_var[0].split(" = ")[1]), single_var[1].split(" = ")[1], single_var[2].split(" = ")[1], single_var[3].split(" = ")[1])
            return sendMail.invoke(self.responce[0]['args'],user_gmail)
        
        return False    
        