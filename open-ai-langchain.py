import uvicorn
import prompts
from pathlib import Path
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI
from fastapi import FastAPI,Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load LLM
load_dotenv()
model = ChatOpenAI(model="gpt-4.1-nano")

# Load FastAPI
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

initialFlow = "" # Debug,Knowledge,Unknown
ruleName = ""
policyNumber = ""
responseMessage = ""
ruleKnowledgeResponseMessage = ""
errorResponseMessage = ""

# Function to set Response Message
def setInitialFlow(rM):
    global initialFlow
    initialFlow = rM

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

# Function to set Response Message
def setRuleKnowledgeResponseMessage(rM):
    global ruleKnowledgeResponseMessage
    ruleKnowledgeResponseMessage = rM

# Function to set Error Response Message
def setErrorResponseMessage(erM):
    global errorResponseMessage
    errorResponseMessage = erM




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



######################## Template to Understand the Initial Flow ( Rule Debugger or Rule Knowledge Base ) ########################

initial_flow_resolver_template = ChatPromptTemplate.from_messages(
    [
        ("system",prompts.prompt_to_understand_initial_query),
        ("human", "{user_query}"),
    ]
)

captureInitialFlowMessageRunnable = RunnableLambda(lambda x: print(f"Captured Initial Flow : {x}") or setInitialFlow(x))
initial_flow_resolver_chain = initial_flow_resolver_template | model | StrOutputParser() | captureInitialFlowMessageRunnable



######################## Template to Send Knowledge Base Response back ########################

knowledge_base_resolver_template = ChatPromptTemplate.from_messages(
    [
        ("system",prompts.prompt_to_fetch_rule_knowledge),
        ("human", "Explain the Rule:{ruleName}. Rule JavaScript:{rule_content}"),
    ]
)

capturKnowledgeBaseMessageRunnable = RunnableLambda(lambda x: print(f"Captured Initial Flow : {x}") or setRuleKnowledgeResponseMessage(x))
knowledge_base_resolver_chain = knowledge_base_resolver_template | model | StrOutputParser() | capturKnowledgeBaseMessageRunnable



######################## Template to Capture Rule Name ########################

capture_ruleName_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpfull assistant responsible for capturing Rule Names, which looks like E343,E211,E.. "
        "from the input prompt. Your response should only contain the rulename. It should be a one word answer."
        "If you are unable to capture the rule name you must respond with 'empty' "),
        ("human", "{user_query}"),
    ]
)

captureRuleNameRunnable = RunnableLambda(lambda x: print(f"Captured Rule Name : {x}") or setRuleName(x))
capture_ruleName_chain = capture_ruleName_template | model | StrOutputParser() | captureRuleNameRunnable


######################## Template to Capture Poilcy Number ########################

capture_policyNumber_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpfull assistant responsible for capturing policyNumber, which looks like 8739217312,312933123 Mostly a set of Integers"
        "from the input prompt. Your response should only contain the policyNumber. It should be a one word answer"),
        ("human", "{user_query}"),
    ]
)

capturePolicyNumberRunnable = RunnableLambda(lambda x: print(f"Captured Policy Number : {x}") or setPolicyNumber(x))
capture_policyNumber_chain = capture_policyNumber_template | model | StrOutputParser() | capturePolicyNumberRunnable


######################## Template to Capture Rule Trigger Analysis Results ########################

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


######################## Template to Capture Rule Trigger Analysis Results ########################

rule_error_resolver_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an assistant which understands Business Rule Management System for an Auto Insurance Company "
        "Looks like the user made an error while prompting for the required details. They could either miss rule number or policy number."
        "Remmember both are required"
        "Provide the response in Markdown Format. No need to includes source code or tables"),
        ("human", "Politely Tell the user about their mistake & keep it a little short."),
    ]
)

captureErrorResponseMessageRunnable = RunnableLambda(lambda x: print(f"Captured Error Response Message : {x}") or setErrorResponseMessage(x))
rule_error_resolver_chain = rule_error_resolver_template | model | StrOutputParser() | captureErrorResponseMessageRunnable




class UserInput(BaseModel):
    user_request: str
    
@app.post("/rulehelp")
def user_request(uInput:UserInput):
    # We need to run the below 2 in . The if else statement looks like a mess, could be fixed later.
    initial_flow_resolver_chain.invoke({"user_query":uInput.user_request})
    if(initialFlow == 'Debug'):
        print("Debug Flow")
        return debug_flow(uInput)
    if(initialFlow == 'Knowledge'):
        print("Knowledge Flow")
        return knowledge_flow(uInput)
    if(initialFlow == 'Unknown'):
        print("Unknown Flow")
        return unknown_flow()


def debug_flow(uInput:UserInput):
    capture_ruleName_chain.invoke({"user_query":uInput.user_request})
    if(ruleName == 'empty'):
        rule_error_resolver_chain.invoke({})
        return Response(content=errorResponseMessage, media_type="text/plain")
    capture_policyNumber_chain.invoke({"user_query":uInput.user_request})
    if(policyNumber == 'empty'):
        rule_error_resolver_chain.invoke({})
        return Response(content=errorResponseMessage, media_type="text/plain")
    print(f"RuleName: {ruleName} , PolicyNumber: {policyNumber}")
    fetchRuleSource()
    fetchPolicyRequest()
    template_pair = {"rule_content":rule_content, "policy_content":policy_content, "ruleName":ruleName , "policyNumber" : policyNumber }
    rule_issue_resolver_chain.invoke(template_pair)
    return Response(content=responseMessage, media_type="text/plain")

def knowledge_flow(uInput:UserInput):
    capture_ruleName_chain.invoke({"user_query":uInput.user_request})
    if(ruleName == 'empty'):
        rule_error_resolver_chain.invoke({})
        return Response(content=errorResponseMessage, media_type="text/plain")
    fetchRuleSource()
    template_pair = {"ruleName":ruleName,"rule_content":rule_content}
    knowledge_base_resolver_chain.invoke(template_pair)
    return Response(content=ruleKnowledgeResponseMessage, media_type="text/plain")

def unknown_flow():
    rule_error_resolver_chain.invoke({})
    return Response(content=errorResponseMessage, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("open-ai-langchain:app", port=5000, log_level="info")
     
