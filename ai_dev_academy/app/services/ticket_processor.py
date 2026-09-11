import asyncio
import random
import logging
from typing import List, Literal
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- 1. Data Models ---
class RawTicket(BaseModel):
    ticket_id: str
    customer_id: str
    issue_description: str

class ProcessedTicket(BaseModel):
    ticket_id: str
    category: Literal["Billing", "Technical", "General"]
    priority_score: int = Field(..., ge=1, le=10)
    summary: str
    needs_escalation: bool

# --- 2. AI Call with Tenacity Retry ---
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(ConnectionError),
    before_sleep=lambda retry_state: logging.warning(
        f"⚠️ فشل الاتصال! إعادة المحاولة رقم {retry_state.attempt_number}..."
    )
)
async def call_ai_model_raw(ticket: RawTicket) -> ProcessedTicket:
    if random.random() < 0.3:
        raise ConnectionError("Timeout/RateLimit error from AI API")

    await asyncio.sleep(random.uniform(0.5, 1.0))
    priority = random.randint(1, 10)
    category = random.choice(["Billing", "Technical", "General"])
    
    return ProcessedTicket(
        ticket_id=ticket.ticket_id,
        category=category,
        priority_score=priority,
        summary=f"مشكلة {category}: {ticket.issue_description[:20]}...",
        needs_escalation=priority > 7
    )

# --- 3. Concurrency Limiter (Semaphore) ---
async def analyze_ticket_with_ai(ticket: RawTicket, semaphore: asyncio.Semaphore) -> ProcessedTicket | None:
    async with semaphore:
        logging.info(f"🔄 جاري تحليل التذكرة [{ticket.ticket_id}]...")
        try:
            result = await call_ai_model_raw(ticket)
            logging.info(f"✅ تم إنهاء التذكرة [{ticket.ticket_id}] - الأولوية: {result.priority_score}")
            return result
        except Exception as e:
            logging.error(f"❌ فشل دائم في معالجة التذكرة [{ticket.ticket_id}]: {e}")
            return None

# --- 4. Main Pipeline ---
async def run_ticket_pipeline(tickets: List[RawTicket]) -> List[ProcessedTicket]:
    rate_limiter = asyncio.Semaphore(3)
    tasks = [analyze_ticket_with_ai(ticket, rate_limiter) for ticket in tickets]
    results = await asyncio.gather(*tasks)
    
    successful_results = [t for t in results if t is not None]
    return successful_results