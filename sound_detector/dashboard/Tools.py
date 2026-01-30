from pydantic import BaseModel, Field
from langchain.tools import tool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from accounts.models import Myuser
import os
from dotenv import load_dotenv
load_dotenv()
sgSecretKey = os.getenv("SENDGRID_API_KEY")
admin_gmail = os.getenv("admin_gmail")

class Schema(BaseModel):
	"""Input for SendMail function"""
	subject : str = Field(description = "A brief alert indicating a detected dangerous situation on bases of primarly focus on  current and historical incidents.")
	plain_text_content : str = Field(description = "A concise plain-text summary of the primarly focus on  current incident and historical context resulting in a danger assessment.")

# function used to send mail
@tool(args_schema = Schema, description = """Sends an alert email when a dangerous situation is detected.
	The email includes a short subject and a plain-text summary
	based on primarly focus on current and historical incidents.""")
# user =Myuser.object.filter()
def sendMail(subject: str, plain_text_content: str,gmail:str):
	print("send mail")
	message = Mail(
		from_email = admin_gmail,
		to_emails =gmail,
		subject = subject,
		plain_text_content = plain_text_content
	)

	print("secret key is ", sgSecretKey)

	if not sgSecretKey:
		raise ValueError("SENDGRID_API_KEY not found")
	try:
		sg = SendGridAPIClient(api_key = sgSecretKey)
		print("message sent")
		responce = sg.send(message)
	except Exception as e:
		raise f"Failed to send email: {str(e)}"
	return True
