import subprocess
import platform
import os
from google import genai
from google.genai import types

# Detect platform
current_platform = platform.system()

# Setup variables exactly as in JS
History = []
ai = genai.Client(api_key="AIzaSyAg_JFo1CiNGpxVCC0nzqGslTMCaIenamU")

#  Tool create karte hai, jo kisi bhi terminal/ shell command ko execute kar sakta hai

def executeCommand(command):
    try:
        # Equivalent to child_process.exec
        # shell=True allows running string commands
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        stdout = result.stdout
        stderr = result.stderr

        if result.returncode != 0:
            # In JS exec, stderr usually implies an error, though sometimes warnings go there too.
            # Python puts errors in stderr if returncode is non-zero.
            return f"Error: {stderr}"

        return f"Success: {stdout} || Task executed completely"

    except Exception as error:
        return f"Error: {error}"

# I am adding this function to fix the "Empty File" issue. 
# executeCommand is bad at writing code into files on Windows.
def createFile(path, content):
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Write content
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: File '{path}' created with content."
    except Exception as error:
        return f"Error writing file: {error}"


executeCommandDeclaration = {
    'name': "executeCommand",
    'description': "Execute a single terminal/shell command. Use this ONLY to create folders (mkdir).",
    'parameters': {
        'type': 'OBJECT',
        'properties': {
            'command': {
                'type': 'STRING',
                'description': 'It will be a single terminal command. Ex: "mkdir calculator"'
            },
        },
        'required': ['command']   
    }
}

createFileDeclaration = {
    'name': "createFile",
    'description': "Create or write content to a file. Use this to write HTML, CSS, JS, or Python code.",
    'parameters': {
        'type': 'OBJECT',
        'properties': {
            'path': {'type': 'STRING', 'description': 'File path (e.g., calculator/index.html)'},
            'content': {'type': 'STRING', 'description': 'The code or text to write in the file'}
        },
        'required': ['path', 'content']
    }
}


availableTools = {
   "executeCommand": executeCommand,
   "createFile": createFile
}


def runAgent(userProblem):

    History.append({
        'role': 'user',
        'parts': [{'text': userProblem}]
    })

    
    while True:
        
        response = ai.models.generate_content(
            model="gemini-2.5-flash", 
            contents=History,
            config=types.GenerateContentConfig(
                system_instruction=f"""You are an Website builder expert. You have to create the frontend of the website by analysing the user Input.
        You have access of tool, which can run or execute any shell or terminal command.
        
        Current user operation system is: {current_platform}
        Give command to the user according to its operating system support.


        <-- What is your job -->
        1: Analyse the user query to see what type of website the want to build
        2: Give them command one by one , step by step
        3: Use available tools.

        // Now you can give them command in following below
        1: First create a folder, Ex: mkdir "calulator" (Use executeCommand)
        2: Inside the folder, create index.html (Use createFile)
        3: Then create style.css same as above (Use createFile)
        4: Then create script.js (Use createFile)
        5: Then write a code in html file (Use createFile)

        You have to provide the terminal or shell command to user, they will directly execute it

        """,
                tools=[{
                    "function_declarations": [executeCommandDeclaration, createFileDeclaration]
                }],
            )
        )


        if response.function_calls:
            
            print(response.function_calls[0])
            # In Python SDK, args is a dictionary
            call = response.function_calls[0]
            name = call.name
            args = call.args 

            # Extract command directly since 'args' is a dict in Python
            # JS: const {name,args} = ... then args is object
            # Here args['command'] holds the value
            
            # Map args to function arguments
            # In JS: func(args). In Python args is {'command': '...'}
            
            if name in availableTools:
                funCall = availableTools[name]
                # Execute function
                result = funCall(**args)
            else:
                result = "Error: Function not found"

            functionResponsePart = {
                'name': name,
                'response': {
                    'result': result,
                },
            }
            
            # model 
            History.append(response.candidates[0].content)

            # result Ko history daalna

            History.append({
                'role': "user",
                'parts': [
                    {
                        'function_response': functionResponsePart,
                    },
                ],
            })
        
        else:

            History.append({
                'role': 'model',
                'parts': [{'text': response.text}]
            })
            print(response.text)
            break


def main():
    print("I am a cursor: let's create a website")
    # Using input() instead of readlineSync.question
    userProblem = input("Ask me anything (or type 'quit' to exit)--> ")

    # --- Added Quit Condition ---
    if userProblem.lower() in ["quit", "exit"]:
        print("Exiting...")
        return
    # ----------------------------

    runAgent(userProblem)
    # Recursion in Python main() is risky for stack overflow, usually loop is better, 
    # but keeping structure as requested:
    main()


if __name__ == "__main__":
    main()