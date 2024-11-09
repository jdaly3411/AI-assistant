from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Speech engine initializatiopn
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id) # 0-Male, 1- # female
activationWord = 'computer' # Single word

# Configure browser 
# Set the path
brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

# Wolfram alpha
appId = '92HK5K-78HQHHKR8J'
wolframClient = wolframalpha.Client(appId)





# Properties for the speech
def speak(text, rate = 150):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

# Understanding what is coming through.
def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    
    return query

# Define a search method for wikipedia
def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query) # Searching wikipedia
    if not searchResults: 
        print('No wikipedia result')
        return 'No result recieved'
    try:
        wikipage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikipage = wikipedia.page(error.options[0])
    print(wikipage.title)
    wikiSummary = str(wikipage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframalpha(query = ''):
    response = wolframClient.query(query)

    # @Success: Wolfram alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods
    if response['@success'] == 'false':
        return 'Could not compute'
    
    # Query resolved
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        # May contain the answer, has the highest confidence value
        # if its primary, or has the title of result or definition, then its the official result
        if(('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            # Remove the b racketed section
            return question.split('(')[0]
            # Search wikipedia instead
            speak('Computation failed. Querying universal databank')
            return search_wikipedia(question)
        



# Main Loop
if __name__ == '__main__':
    speak('All systems operational.')

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0) 

            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings.')
                else:
                    query.pop(0) #  Remove say
                    speech = ' '.join(query)
                    speak(speech)
                
            # Navigating to a website
            if query[0] == 'go' and query[1] == "to":
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('brave').open_new(query)
            
            # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank')
                speak(search_wikipedia(query))
            
           # Wolfram Alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Computing')
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to compute.')
            
            # Note taking
            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-$m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak('Note Written')

            if query[0] == 'exit':
                speak('Goodbye')
                break

            






