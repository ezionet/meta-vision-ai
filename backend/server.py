"""Minimal image-analysis API. Run with uvicorn server:app --host 127.0.0.1 --port 8000."""
import base64
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

app = FastAPI(title='Meta Vision AI', version='0.1.0')

class PhotoRequest(BaseModel):
    image_base64: str = Field(min_length=32, max_length=15_000_000)
    question: str = Field(default='Analizza questa immagine e suggerisci verifiche tecniche.', max_length=1500)

@app.post('/analyze')
async def analyze(payload: PhotoRequest):
    if not os.getenv('OPENAI_API_KEY'):
        raise HTTPException(503, 'OPENAI_API_KEY not configured')
    try:
        raw = base64.b64decode(payload.image_base64, validate=True)
        if not raw.startswith(b'\xff\xd8\xff') and not raw.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Only JPEG or PNG supported')
        if len(raw) > 8_000_000:
            raise ValueError('Image too large')
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc
    mime = 'image/jpeg' if raw.startswith(b'\xff\xd8\xff') else 'image/png'
    client = AsyncOpenAI()
    response = await client.responses.create(
        model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
        store=False,
        instructions=('Sei un assistente tecnico IT. Rispondi in italiano in modo conciso. '
                      'Distingui fatti visibili da ipotesi; evita di inventare dettagli. '
                      'Prima di suggerire modifiche rischiose, chiedi verifiche.'),
        input=[{'role':'user','content':[
            {'type':'input_text','text':payload.question},
            {'type':'input_image','image_url':f'data:{mime};base64,{payload.image_base64}'}
        ]}]
    )
    return {'answer':response.output_text}
