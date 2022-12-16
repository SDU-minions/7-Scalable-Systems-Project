package com.example.scalablesystems



import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import android.util.Log
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.api.gax.core.FixedCredentialsProvider
import com.google.auth.oauth2.GoogleCredentials
import com.google.cloud.dialogflow.v2.*
import kotlinx.coroutines.Dispatchers.Default
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.*


class MainActivity : AppCompatActivity() {
    //Dialogflow: https://github.com/veeyaarVR/dialogflow_android_kotlin
    //Speech to text: https://www.geeksforgeeks.org/speech-to-text-application-in-android-with-kotlin/#video

    //dialogFlow
    private var sessionsClient: SessionsClient? = null
    private var sessionName: SessionName? = null
    private val uuid = UUID.randomUUID().toString()
    private val TAG = "mainactivity"

    //if mic on/ isnt on computer
    private var mic: Boolean = true

    // on below line we are creating variables
    // for text view and image view
    lateinit var outputTV: TextView
    lateinit var micIV: ImageView
    lateinit var micText: TextView
    lateinit var resultOutput: TextView

    // on below line we are creating a constant value
    private val REQUEST_CODE_SPEECH_INPUT = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        supportActionBar?.hide()


        //initialize mic config
        // initializing variables of list view with their ids.
        outputTV = findViewById(R.id.idTVOutput)
        micIV = findViewById(R.id.idIVMic)
        micText = findViewById(R.id.idMicText)
        resultOutput = findViewById(R.id.idResultOutput)

        // on below line we are adding on click
        // listener for mic image view.
        micIV.setOnClickListener {
            // on below line we are calling speech recognizer intent.
            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)

            // on below line we are passing language model
            // and model free form in our intent
            intent.putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )

            // on below line we are passing our
            // language as a default language.
            intent.putExtra(
                RecognizerIntent.EXTRA_LANGUAGE,
                Locale.getDefault()
            )

            // on below line we are specifying a prompt
            // message as speak to text on below line.
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to text")

            // on below line we are specifying a try catch block.
            // in this block we are calling a start activity
            // for result method and passing our result code.
            try {
                startActivityForResult(intent, REQUEST_CODE_SPEECH_INPUT)
            }  catch (e: Exception) {
                // on below line we are displaying error message in toast
                    //If no mic, then
               /* Toast
                    .makeText(
                        this@MainActivity, " " + e.message,
                        Toast.LENGTH_SHORT
                    )
                    .show()*/
                mic = false
                micIV.setOnClickListener{setText("no mic")}
                micText.setText("Click on mic to change between intents ")
            }
        }

       //HiveConnection.connect()

    }

    private fun setText(message: String) {
        runOnUiThread { outputTV.setText(message) }
    }

    private fun showResult(result: String){
        runOnUiThread{
            resultOutput.setText(result)
            resultOutput.visibility = View.VISIBLE
        }
    }

    private fun hideResult(){
        runOnUiThread{
            resultOutput.visibility = View.INVISIBLE
        }
    }


    private fun setUpBot() {
        try {
            val stream = this.resources.openRawResource(R.raw.credentials)
            val credentials: GoogleCredentials = GoogleCredentials.fromStream(stream)
                .createScoped("https://www.googleapis.com/auth/cloud-platform")
            val projectId: String = "myfirstagent-htrt"
            val settingsBuilder: SessionsSettings.Builder = SessionsSettings.newBuilder()
            val sessionsSettings: SessionsSettings = settingsBuilder.setCredentialsProvider(
                FixedCredentialsProvider.create(credentials)
            ).build()
            sessionsClient = SessionsClient.create(sessionsSettings)
            sessionName = SessionName.of(projectId, uuid)
            Log.d(TAG, "projectId : $projectId")
        } catch (e: Exception) {
            Log.d(TAG, "setUpBot: " + e.message)
        }
    }


    private fun sendMessageToBot(message: String) {
        val input = QueryInput.newBuilder()
            .setText(TextInput.newBuilder().setText(message).setLanguageCode("en-US")).build()
        GlobalScope.launch {
            sendMessageInBg(input, message)
        }


    }

    private suspend fun sendMessageInBg(
        queryInput: QueryInput, message: String
    ) {
        withContext(Default) {
            try {
                val detectIntentRequest = DetectIntentRequest.newBuilder()
                    .setSession(sessionName.toString())
                    .setQueryInput(queryInput)
                    .build()
                val result = sessionsClient?.detectIntent(detectIntentRequest)

                if (result != null) {
                    val botReply: String = result.queryResult.intent.displayName
                    Log.i(TAG, botReply)
                    if (botReply == "Default Welcome Intent" || botReply ==  "Default Fallback Intent"){
                        setText("Git Genie does not understand, try again")
                    } else {
                        setText(message)
                        updateUI(botReply)
                    }

                }

            } catch (e: java.lang.Exception) {
                Log.d(TAG, "doInBackground: " + e.message)
                e.printStackTrace()
            }
        }
    }

    private fun updateUI(intent: String){
        hideResult()
        if(mic){
            when (intent) {
                "How many commits have been made the last specified hours?" -> {
                    showResult("42")
                }
                "How many commits on average does each programming language have?" -> {
                    showResult("Java has 1056 commits")
                }
                "What are the top x programming languages used in y time" -> {
                    return
                }
                "What is the latest commit on GitHub?" -> {
                    showResult("The latest commit is super awesome!!")
                }
                "What is the most active repository the last specified hours?" -> {
                    showResult("The most active repository is Git Genie")
                }
            }
        } else {

        }

    }


    // on below line we are calling on activity result method.
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        // in this method we are checking request
        // code with our result code.
        if (requestCode == REQUEST_CODE_SPEECH_INPUT) {
            // on below line we are checking if result code is ok
            if (resultCode == RESULT_OK && data != null) {

                // in that case we are extracting the
                // data from our array list
                val array: ArrayList<String> = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS) as ArrayList<String>
                val res: String = array[0]
                Log.i(TAG, res)


                //initialize bot config
                setUpBot()
                sendMessageToBot(res)

            }
        }
    }




}
