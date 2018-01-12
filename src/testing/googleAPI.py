from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def sentimentAnalysis(text):
    client = language.LanguageServiceClient()
    sentiment = client.analyze_sentiment(types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT))
    return sentiment

sentiment = sentimentAnalysis("This is making me sad")
print(sentiment) #.document_sentiment