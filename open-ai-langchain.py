from pathlib import Path
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI

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
        ("human", "Why is the rule E101 triggered on my policy 9881923218"),
    ]
)

captureRuleNameRunnable = RunnableLambda(lambda x: print(f"Captured Rule Name : {x}") or setRuleName(x))
capture_ruleName_chain = capture_ruleName_template | model | StrOutputParser() | captureRuleNameRunnable


# Template to Capture Policy Number
capture_policyNumber_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpfull assistant responsible for capturing policyNumber, which looks like 8739217312,312933123 Mostly a set of Integers"
        "from the input prompt. Your response should only contain the policyNumber. It should be a one word answer"),
        ("human", "Why is the rule E101 triggered on my policy 9881923218"),
    ]
)

capturePolicyNumberRunnable = RunnableLambda(lambda x: print(f"Captured Policy Number : {x}") or setPolicyNumber(x))
capture_policyNumber_chain = capture_policyNumber_template | model | StrOutputParser() | capturePolicyNumberRunnable

# We need to run the below 2 in parallel
capture_ruleName_chain.invoke({})
capture_policyNumber_chain.invoke({})

print(f"RuleName: {ruleName} , PolicyNumber: {policyNumber}")

# Fetch Rule File Source 
file_path = Path('Rules/' + ruleName + '.js')
rule_content = file_path.read_text()
# print(rule_content)

# Fetch Policy Request File Source 
file_path = Path('PolicyRequest/'+ policyNumber + '.json')
policy_content = file_path.read_text()
# print(policy_content)

rule_issue_resolver_template = ChatPromptTemplate.from_messages(
    [
        ("system","You are an assistant which understands Business Rule Management System for an Auto Insurance Company where the rules are written in JavaScript and the input request to those are in JSON format."
        "Provide the response in Markdown Format"),
        ("human", "Why is the rule {ruleName} Triggered on my policy {policyNumber} ? What are the critera for the Rule ? What Data can I change in my policy to avoid it ? Rule Data :  {rule_content} "
        "Policy Data : {policy_content}"),
    ]
)

captureResponseMessageRunnable = RunnableLambda(lambda x: print(f"Captured Response Message : {x}") or setResponseMessage(x))
rule_issue_resolver_chain = rule_issue_resolver_template | model | StrOutputParser() | captureResponseMessageRunnable

template_pair = {"rule_content":rule_content, "policy_content":policy_content, "ruleName":ruleName , "policyNumber" : policyNumber }

rule_issue_resolver_chain.invoke(template_pair)
