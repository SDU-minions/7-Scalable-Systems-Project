from pyhive import hive
import os
from os import devnull
from google.cloud import dialogflow
import speech_recognition as sr
from contextlib import redirect_stdout

r = sr.Recognizer()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'myfirstagent-htrt'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = 'me'

def hive_query(query):
    conn = hive.connect(host='localhost', port=10000, username='hive', password='hive', auth='CUSTOM', database='default')
    cursor = conn.cursor()
    cursor.execute(query)
    out = cursor.fetchall()
    conn.close()
    return out

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    #print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        #print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        return response.query_result.fulfillment_text

def speech_to_text():
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")

        try:
            with redirect_stdout(open(devnull, 'w')) as fnull:
                res = r.recognize_google(audio_text)
            print("Captured text: " + res)
        except:
            res = ""
            print("Sorry, I did not get that, please try again")
        return res

if __name__ == '__main__':
    
    while True:
        if(input("Press Enter to start talking...\n") == 'exit'):
            break
        query_text = [speech_to_text()]
        if(query_text == ['']):
            continue
        query_intent = detect_intent_texts(DIALOGFLOW_PROJECT_ID, SESSION_ID, query_text, DIALOGFLOW_LANGUAGE_CODE)
        if query_intent == '':
            continue
        output = hive_query(query_intent)

        print("="*20)
        print("The result is: ")
        for i in output:
            print(i)
        print("="*20)

