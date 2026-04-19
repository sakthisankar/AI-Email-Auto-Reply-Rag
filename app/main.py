from app.gmail_service import authenticate_gmail, read_emails, create_draft
from app.rag_pipeline import load_kb, create_or_load_db, retrieve_context
from app.llm_service import generate_reply

def main():
    service = authenticate_gmail()
    emails = read_emails(service)

    kb_data = load_kb()
    db = create_or_load_db(kb_data)

    for msg_id, thread_id, text, sender, subject in emails:
        context = retrieve_context(db, text)
        reply = generate_reply(context, text)

        create_draft(service, thread_id, reply, sender, subject)
