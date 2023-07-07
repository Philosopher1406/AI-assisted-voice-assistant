import speech_recognition as sr
import pyttsx3
import datetime
import sys
import webbrowser
import time
import os
import wikipedia
import openai
import smtplib
import wolframalpha
import pyjokes




r = sr.Recognizer()
engine = pyttsx3.init()
openai.api_key="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"



class Assistant:
    def __init__(self, name, todos):
        self.name = name
        self.todos = todos

    def greet(self):
        return f'Hello, I am a {self.name} the voice assistant. How can I assist you today?'

    def speak(self, speech):
        engine.say(speech)
        engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            audio = r.listen(source)
            command = ''
            try:
                command = r.recognize_google(audio)
            except sr.UnknownValueError:
                self.speak("Sorry, can you please repeat that?")
            except sr.RequestError:
                self.speak(
                    "My apologies, my speech service is down. Please try again later.")
                sys.exit()
            print(command)
            return command
        
    '''def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your email id', 'your email password')
        server.sendmail('your email id', to, content)
        server.close()'''
    

    def cant_do(self):
        self.speak("Sorry, I do not have that ability yet.")

    # Respond to the command given by the user
    def respond(self, command):
        # if the name of the instance is in the command
        while True:
            if self.name.lower() in command:
                self.speak("Yes")

            elif  self.listen() == "stop":
                self.speak("Okay, I'll stop talking now.")
                break

            elif "what is the time" in command:
                now = datetime.datetime.now()
                hours = now.strftime("%H")
                if hours > str(12):
                    hours = int(hours) - 12
                elif hours == '00':
                    hours = int(hours) + 12
                self.speak(now.strftime(f"{str(hours)}:%M %p"))
            


            elif "exit" in command:
                self.speak("Goodbye, have a nice day.")
                sys.exit()

            elif "Google" in command:
                self.speak('What would you like to search for?')
                print("ask for something to search for...")
                print("Listening...")
                query = self.listen()
                webbrowser.open("https://google.com/search?query="+query)


            elif "GPT" in command:
                self.speak('What would you like to search for?')
                print("ask for something to search for...")
                print("Listening...")
                results =openai.Completion.create(engine="text-davinci-003", prompt = self.listen(),max_tokens=1000)
                self.speak("According to chatGPT")
                print(results.choices[0]['text'])
                self.speak(results.choices[0]['text'])
        
        
            elif "YouTube" in command:
                self.speak('What would you like to search for?')
                print("ask for something to search for...")
                print("Listening...")
                query = self.listen()
                webbrowser.open("https://www.youtube.com/results?search_query="+query)

            elif "Wikipedia" in command:
                self.speak('What would you like to search for?')
                print("ask for something to search for...")
                print("Listening...")
                query = self.listen()
                results = wikipedia.summary(query,auto_suggest=False,redirect=True,sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)

            elif 'play music' in command:
                music_dir = 'C:\music'
                songs = os.listdir(music_dir)
                print(songs)    
                os.startfile(os.path.join(music_dir, songs[0]))


            elif "to do" in command:
                self.speak("What would you like to do")
                if "add" in command:
                    self.speak("What would you like to add?")
                    print("Say a to-do that you would like to add...")
                    print("Listening...")
                    todo = self.listen()
                    self.todos.append(todo)
                    while todo=="":
                        self.speak("I could not catch that,please repeat")
                        break
                    todo=self.listen()
                    self.todos.append(todo)
                    self.speak("Your to-do has successfully been added.")
                    print("Your to-dos ->", self.todos)
                    f1 = open(f'todo.txt', 'w')
                    f1.write(todo)
                    f1.close()


                if "remove" in command:
                    self.speak("What to-do would you like to remove?")
                    print("Say a to-do that you would like to remove", self.todos)
                    print("Listening...")
                    todo = self.listen()
                    if todo not in self.todos:
                        self.speak(
                    "That to-do does not exist. If you meant to say a different to-do, please ask to remove a to-do again.")
                        print("Listening...")
                        todo = self.listen()
                    if todo in self.todos:
                        self.todos.remove(todo)
                        self.speak("Your to-do has been successfully removed.")
                        print("Your to-dos ->", self.todos)

                if "show" in command:
                    self.speak("Here are your to-dos.")
                    self.speak(self.todos)
                    print("Your to-dos ->", self.todos)
                    f1 = open(f'todo.txt', 'r')

            elif "what day is it" in command:
                self.speak(
                    f'Today is {datetime.datetime.today().strftime("%A")}, {datetime.date.today().strftime("%B %d, %Y")}')
            
            elif 'how are you' in command:
                self.speak("I am fine, Thank you")
                self.speak("How are you, Sir")
 
            elif 'fine' in command or "good" in command:
                self.speak("It's good to know that your fine")

            elif 'joke' in command:
                self.speak(pyjokes.get_joke())

            elif 'calculate' in command:
             
                app_id = 'WRJUHK-KJ73AKH5YL'
                client = wolframalpha.Client(app_id)
                self.speak("What would you like to calculate")
                query = self.listen()
                res = client.query(query)
                output = next(res.results).text
                print(output)
                self.speak(output)

           

            elif "create a file" in command:
                self.speak("What would you like the filename to be?")
                print("Say the file name...")
                filename = self.listen()
                # Create a file if that file does not exist.
                new_file = open(f'{filename}.txt', 'x')
                self.speak(
                "Your file has been successfully created. Would you like to edit this file?")
                print("Listening...")
                usr_response = self.listen()

                if 'yes' in usr_response:
                    self.speak("What would you like to write in this file?")
                    file = open(f"{filename}.txt", 'a')
                    print("Start listing the contents of this file...")
                    file_content = self.listen()
                    file.write(file_content)
                    file.close()
                    self.speak("Your content has successfully been added.")
                    print("Saved!")

                if 'no' in usr_response:
                    self.speak("Okay.")
                    print("No changes will be added to this file.")

            elif "edit a file" in command:
                self.speak("What file would you like to edit?")
                print("Please say the file name that you would like to edit...")
                filename = self.listen()

                if os.path.exists(f"{filename}.txt"):
                    self.speak("What would you like to add to this file?")
                    print("List what you would like to add to this file.")
                    action = self.listen()
                    if action == 'add':
                        self.speak("What would you like to add to this file?")
                        file = open(f"{filename}.txt", 'a')
                        print("Say something you would like to add to this file.")
                        add = self.listen()
                        file.write("\n"+add)
                        file.close()
                        self.speak("Your content has been successfully added.")
                        print("Saved!")
                    else:
                        self.speak("That action does not exist.")
                else:
                    self.speak("That file does not exist.")

            elif "delete a file" in command:
                self.speak("What file would you like to delete?")
                print("Please say the file that you would like to delete...")
                filename = self.listen()
                if os.path.exists(f'{filename}.txt'):
                    os.remove(f'{filename}.txt')
                    self.speak("Your file has been removed.")
                else:
                    self.speak("Sorry, that file does not exist.")

            else:
                self.cant_do()


# Create assistant
assistant = Assistant("jarvis", [])

# Get the assistant's greeting
greeting = assistant.greet()

# Use the speak() method and pass in the greeting to greet the user
assistant.speak(greeting)

print("Listening...")
while True:
    # This command variable contains what command was said to the assistant and prints it.
    command = assistant.listen()
    assistant.respond(command)
    