from tools import DocumentTools

result = DocumentTools().list_files("transcripts")
print(f"Files in folder 'transcripts': {result} type {type(result)}")


doc = DocumentTools().read_docx("transcripts/ThreatMark Discussion SQR.docx")
print(f"type {type(doc)}\n and Content of 'ThreatMark Discussion SQR.docx': {doc}")
