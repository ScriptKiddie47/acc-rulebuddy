import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI
from fastapi import FastAPI,Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return "Up"


load_dotenv()
model = ChatOpenAI(model="gpt-4.1-nano")

ruleName = ""
policyNumber = ""
responseMessage = ""

# Function to set ruleName
def setRuleName(rN):
    global ruleName
    ruleName = rN

# Function to set policyNumber
def setPolicyNumber(pN):
    global policyNumber
    policyNumber = pN

# Function to set Response Message
def setResponseMessage(rM):
    global responseMessage
    responseMessage = rM


# Template to Capture Rule Name
capture_ruleName_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpfull assistant responsible for capturing ruleName, which looks like E343,E211,E.. "
        "from the input prompt. Your response should only contain the rulename. It should be a one word answer"),
        ("human", "{user_query}"),
    ]
)

captureRuleNameRunnable = RunnableLambda(lambda x: print(f"Captured Rule Name : {x}") or setRuleName(x))
capture_ruleName_chain = capture_ruleName_template | model | StrOutputParser() | captureRuleNameRunnable


# Template to Capture Policy Number
capture_policyNumber_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpfull assistant responsible for capturing policyNumber, which looks like 8739217312,312933123 Mostly a set of Integers"
        "from the input prompt. Your response should only contain the policyNumber. It should be a one word answer"),
        ("human", "{user_query}"),
    ]
)

capturePolicyNumberRunnable = RunnableLambda(lambda x: print(f"Captured Policy Number : {x}") or setPolicyNumber(x))
capture_policyNumber_chain = capture_policyNumber_template | model | StrOutputParser() | capturePolicyNumberRunnable

# Fetch Rule File Source
def fetchRuleSource():
    global rule_content
    file_path = Path('Rules/' + ruleName + '.js')
    rule_content = file_path.read_text()
    # print(rule_content)

# Fetch Policy Request File Source 
def fetchPolicyRequest():
    global policy_content
    file_path = Path('PolicyRequest/'+ policyNumber + '.json')
    policy_content = file_path.read_text()
    # print(policy_content)

rule_issue_resolver_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an assistant which understands Business Rule Management System for an Auto Insurance Company "
        "where the rules are written in JavaScript and the input request to those are in JSON format."
        "Provide the response in Markdown Format. No need to includes source code or tables"),
        ("human", "Why is the rule {ruleName} Triggered on my policy {policyNumber} ? What are the critera for the Rule ? "
        "What Data can I change in my policy to avoid it ? Rule Data :  {rule_content} "
        "Policy Data : {policy_content}"),
    ]
)

captureResponseMessageRunnable = RunnableLambda(lambda x: print(f"Captured Response Message : {x}") or setResponseMessage(x))
rule_issue_resolver_chain = rule_issue_resolver_template | model | StrOutputParser() | captureResponseMessageRunnable



class UserInput(BaseModel):
    user_request: str
    
@app.post("/rulehelp")
def user_request(uInput:UserInput):
    # We need to run the below 2 in parallel
    capture_ruleName_chain.invoke({"user_query":uInput.user_request})
    capture_policyNumber_chain.invoke({"user_query":uInput.user_request})
    print(f"RuleName: {ruleName} , PolicyNumber: {policyNumber}")
    fetchRuleSource()
    fetchPolicyRequest()
    template_pair = {"rule_content":rule_content, "policy_content":policy_content, "ruleName":ruleName , "policyNumber" : policyNumber }
    rule_issue_resolver_chain.invoke(template_pair)
    return Response(content=responseMessage, media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run("open-ai-langchain:app", port=5000, log_level="info")