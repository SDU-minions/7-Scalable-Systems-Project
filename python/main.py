from pyhive import hive
from flask import Flask
import os
from google.cloud import dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
app = Flask(__name__)

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
    print("Session path: {}\n".format(session))

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
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


@app.route('/')
def hello_world():
    #detect_intent_texts(DIALOGFLOW_PROJECT_ID, SESSION_ID, ['top commits'], DIALOGFLOW_LANGUAGE_CODE)
    #for result in hive_query("SELECT * FROM repos LIMIT 10"):
    #    print(result)
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)