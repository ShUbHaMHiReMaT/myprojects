import PyPDF2
from googletrans import Translator
import pyttsx3
import asyncio

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    if file_path.startswith('file:///'):
        file_path = file_path[8:]
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from a text file
def extract_text_from_txt(file_path):
    if file_path.startswith('file:///'):
        file_path = file_path[8:]
    with open(file_path, 'r') as file:
        return file.read()

# Function to translate text into multiple languages
async def translate_text(text, dest_language):
    translator = Translator()
    translated = await translator.translate(text, dest=dest_language)
    return translated.text

# Function to convert text to speech
def text_to_speech(text, language='en'):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to analyze the medical report
def analyze_report(text, detail_level='basic'):
    report_summary = ""
    recommendations = ""

    if "diabetes" in text.lower():
        report_summary += "**Condition Detected:** Diabetes\n"
        if detail_level == 'detailed':
            report_summary += (
                "Diabetes is a chronic metabolic disorder where the body is unable to effectively process glucose, "
                "leading to elevated blood sugar levels. It can be classified into Type 1 and Type 2. Symptoms include "
                "excessive thirst, frequent urination, and fatigue. If left unmanaged, it can lead to complications."
            )
        recommendations += (
            "- Monitor blood sugar regularly.\n"
            "- Balanced diet with fiber and lean proteins.\n"
            "- Regular exercise.\n"
            "- Consult an endocrinologist.\n"
        )

    if "cancer" in text.lower():
        report_summary += "**Condition Detected:** Cancer\n"
        if detail_level == 'detailed':
            report_summary += (
                "Cancer involves uncontrolled growth of abnormal cells. Symptoms vary depending on type, including "
                "persistent fatigue and weight loss. Early detection is crucial.\n"
            )
        recommendations += (
            "- Consult an oncologist immediately.\n"
            "- Undergo diagnostic tests.\n"
            "- Discuss treatment options like chemotherapy.\n"
        )

    if "hypertension" in text.lower() or "high blood pressure" in text.lower():
        report_summary += "**Condition Detected:** Hypertension\n"
        if detail_level == 'detailed':
            report_summary += (
                "Hypertension is high blood pressure, increasing risks of heart disease and stroke. Often symptomless.\n"
            )
        recommendations += (
            "- Monitor blood pressure regularly.\n"
            "- Reduce sodium, healthy diet.\n"
            "- Exercise regularly.\n"
            "- Stress management techniques.\n"
        )

    if not report_summary:
        report_summary = "No specific medical conditions detected.\n"
        recommendations = (
            "- Maintain a balanced diet.\n"
            "- Regular physical activity.\n"
            "- Stay hydrated and sleep well.\n"
        )

    return report_summary + "\n**Recommendations:**\n" + recommendations

# Main function to interact with the user
async def main():
    file_path = input("Enter the path to the medical report (PDF or TXT): ")
    language = input("Choose language (en for English, hi for Hindi, kn for Kannada): ")
    read_aloud = input("Would you like the report to be read aloud? (yes/no): ")
    detail_level = input("Choose analysis level (basic/detailed): ")

    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.txt'):
        text = extract_text_from_txt(file_path)
    else:
        print("Unsupported file format. Please use PDF or TXT.")
        return

    analysis = analyze_report(text, detail_level)

    if language != 'en':
        translated_analysis = await translate_text(analysis, language)
    else:
        translated_analysis = analysis

    print("\nMedical Report Analysis:\n")
    print(translated_analysis)

    if read_aloud.lower() == 'yes':
        text_to_speech(translated_analysis, language)

if __name__ == "__main__":
    asyncio.run(main())
