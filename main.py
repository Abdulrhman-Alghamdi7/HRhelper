
import openai
import time
import pandas as pd 

api_key = "api_key"
client = openai.Client(api_key=api_key)

# Create thread and assistant with delays
thread = client.beta.threads.create()
time.sleep(2)

assis = client.beta.assistants.create(
    name='Recruitment assistant',
    instructions='You are a Recruitment assistant to extract the important information from job requests',
    tools=[],
    model='gpt-3.5-turbo-1106'
)
time.sleep(2)

def askassis(q):
    message = client.beta.threads.messages.create(thread_id=thread.id, role='user', content=q)

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assis.id)

    timeout_seconds = 60  # Set your desired timeout in seconds
    start_time = time.time()

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.completed_at is not None:
            break

        if time.time() - start_time > timeout_seconds:
            print("Timeout reached. Exiting loop.")
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = []
    for i in messages.data:
        if i.role == 'assistant':
            for c in i.content:
                if c.type == 'text':
                    response.append(c.text.value)
    
    return response[0]
reqs = []
info = [['desired company','desired job title','degree','field of the degree','experience time','experience industry','Key Skills and Expertise','Previous Company','Significant Achievement or Project','Relevant Skill or Competency','Phone Number','Email Address', 'Name']]

c = 1
for i in reqs:
    info.append(((askassis("Extract details from the job request in the specified format: [desired company, desired job title, degree, field of the degree, experience time, experience industry, Key Skills and Expertise, Previous Company, Significant Achievement or Project, Relevant Skill or Competency, Phone Number, Email Address, Name]. Use 'null' in the respective order for any unspecified or irrelevant information. Ensure that the provided information aligns accurately with the format, avoiding additional commas or details outside the specified structure. The job request : "+i))[1:-1]).split(','))
    print(str((c/len(reqs))*100)+'%')
    c+=1
    if i != len(reqs)+1:
        time.sleep(15)

data = pd.DataFrame(info)
data.to_csv('reqs.csv',index=False, header=False)







