# Tasks related to ExamSession have been removed. Placeholder for future tasks.

# Example placeholder task
from celery import shared_task

@shared_task
def placeholder_task():
    return "No operation"

import os
import json
from openai import OpenAI
from .models import ExamSession
from django.utils import timezone

# Groq uses OpenAI-compatible API — just change base_url and api_key
client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1",
)

# Best free Groq model for conversation
GROQ_CHAT_MODEL = "llama-3.3-70b-versatile"

@shared_task
def process_chat_message(session_id):
    try:
        session = ExamSession.objects.get(id=session_id)
        
        # Prepare messages
        messages = [{"role": "system", "content": session.system_prompt_used}]
        messages.extend(session.chat_history)
        
        # Call Groq (same API as OpenAI)
        response = client.chat.completions.create(
            model=GROQ_CHAT_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )
        
        ai_message = response.choices[0].message.content
        
        # Append AI response to chat history
        history = list(session.chat_history)
        history.append({"role": "assistant", "content": ai_message})
        session.chat_history = history
        session.save()
        return True
    except Exception as e:
        print(f"Error processing chat: {e}")
        return False


@shared_task
def finalize_exam_evaluation(session_id):
    """
    Groq does not support structured outputs (beta.parse),
    so we ask for JSON manually and parse it ourselves.
    """
    try:
        session = ExamSession.objects.get(id=session_id)
        
        system_msg = (
            "Siz ekspert imtihon qabul qiluvchisiz. "
            "Quyidagi rolli o'yin suhbatini tahlil qiling va JSON formatda baho bering.\n"
            "Javob FAQAT quyidagi JSON tuzilmasida bo'lsin, boshqa matn bo'lmasin:\n"
            '{"score": <0-100>, "strengths": ["...", "..."], "weaknesses": ["...", "..."], "recommendations": "..."}'
        )
        
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in session.chat_history])
        user_msg = (
            f"Ssenariy: {session.system_prompt_used}\n\n"
            f"Suhbat:\n{chat_text}"
        )
        
        response = client.chat.completions.create(
            model=GROQ_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        
        raw = response.choices[0].message.content.strip()
        
        # Extract JSON even if the model adds some surrounding text
        start = raw.find('{')
        end = raw.rfind('}') + 1
        evaluation = json.loads(raw[start:end])
        
        session.score = int(evaluation.get('score', 0))
        session.feedback = evaluation
        session.completed_at = timezone.now()
        session.save()
        return True
    except Exception as e:
        print(f"Error finalizing exam: {e}")
        return False
