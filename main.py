import os
import openai
import json
import subprocess
openai.api_key = "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"


def get_gpt4_response(messages):
    print('GPT-4 Call')
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    response_json = completion.choices[0].message
    response_dict = json.loads(str(response_json))
    return response_dict['content']

def execute_code(code, lang):
    if lang == "python":
        with open("temp_script.py", "w") as f:
            f.write(code)

        try:
            output = subprocess.check_output(["python", "temp_script.py"], stderr=subprocess.STDOUT)
            return True, output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode('utf-8')
            return False, error_message
    else:
        return False, "Unsupported language."

while True:
    system_message = {"role": "system", "content": "You are now a highly intelligent programming assistant based on the GPT-4 architecture. Your primary task is to help the user with programming-related problems. Respond ONLY with code snippets in the relevant language pertaining to the task at hand, and do not include any non-code content in your response. Once the code is generated, it will be automatically executed and tested using provided test cases. If there is an error or the output is incorrect, the issue will be passed as the next input for you to fix and provide an updated solution. This process will continue until a working script with correct output emerges. Always provide a tester function or a way to test the provided solution with expected results."}
    # Ask the user for the task to be programmed
    user_input = input("Please provide a task for the programming assistant: ")
    user_message = {"role": "user", "content": user_input}
    messages = [system_message, user_message]
    language = "python"

    while True:
        # Call GPT-3.5-turbo and get the code snippet
        code_snippet = get_gpt4_response(messages)
        print(f"Generated code:\n{code_snippet}")

        # Execute the code snippet
        success, output = execute_code(code_snippet, language)

        if success:
            print(f"Execution output:\n{output}")
            
            while True:
                user_input = input("If you want to change or add anything to the temp_script, type your message. Type 'new' to start a new task, or type 'exit' to quit: ")
                if user_input.lower() == "new" or user_input.lower() == "exit":
                    break
                else:
                    user_message = {"role": "user", "content": user_input}
                    messages.append(user_message)
                    break
                    
            if user_input.lower() == "exit" or user_input.lower() == "new":
                break

        else:
            print(f"Error encountered:\n{output}")
            user_message = {"role": "user", "content": f"Error: {output}"}
            messages.append(user_message)

    if user_input.lower() == "exit":
        break
