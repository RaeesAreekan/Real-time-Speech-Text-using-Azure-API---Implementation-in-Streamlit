import azure.cognitiveservices.speech as speechsdk
import config
import streamlit as st

# Replace with your Azure Speech subscription key and region
SPEECH_KEY = config.SPEECH_KEY
SPEECH_REGION = config.SPEECH_REGION


def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY, region=SPEECH_REGION
    )
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    output_text = st.empty()

    def speech_recognized_callback(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            output_text.text("Recognized: {}".format(result.text))
            st.write("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    speech_recognizer.recognized.connect(speech_recognized_callback)
    speech_recognizer.start_continuous_recognition()

    input("Press Enter to stop...\n")

    speech_recognizer.stop_continuous_recognition()


st.title("Speech to Text")
# def start_recognition():
#     recognize_thread = Thread(target=recognize_from_microphone)
#     recognize_thread.daemon = True
#     recognize_thread.start()
recognize_from_microphone()

# st.title("Speech to Text")
# if __name__ == "__main__":
#     start_recognition()  # Start the speech recognition thread
#     st.write("Listening...")  # Show the user that we're listening
#     st.write(output)
