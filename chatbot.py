# chatbot.py
# Trợ lý Lễ tân Ảo StayEasy Concierge
import os
import glob
import re
from openai import OpenAI
import time

# ------------------------------
# CONFIG
# ------------------------------
MODEL = "gemini-2.5-flash"
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yte")
MAX_TOKENS = 600
RETRY_DELAY = 5
MAX_RETRIES = 3

# ------------------------------
def load_md_data(folder):
    database = {}
    for path in glob.glob(os.path.join(folder, "*.md")):
        name = os.path.basename(path).replace(".md", "")
        try:
            with open(path, "r", encoding="utf-8") as f:
                database[name] = f.read()
        except Exception as e:
            print(f"⚠️ Không load được file {path}: {e}")
    return database

def retrieve_context(db, question):
    score_list = []
    q_words = re.findall(r"\w+", question.lower())
    for name, content in db.items():
        score = sum(1 for w in q_words if w in content.lower())
        score_list.append((score, name, content))
    score_list.sort(reverse=True, key=lambda x: x[0])
    top_matches = [c for s, n, c in score_list[:3] if s > 0]
    return "\n\n".join(top_matches) if top_matches else "\n\n".join(db.values())

class StayEasyChatbot:
    def __init__(self, model=MODEL):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("⚠️ Không tìm thấy GEMINI_API_KEY trong biến môi trường!")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = model
        self.db = load_md_data(DATA_FOLDER)
        print(f"✅ Đã load {len(self.db)} tài liệu thông tin homestay StayEasy.")

    def ask(self, question):
        context = retrieve_context(self.db, question)

        system_prompt = (
            "Bạn là trợ lý ảo thân thiện StayEasy Homestay Assistant của hệ thống Homestay Nghỉ Dưỡng StayEasy. "
            "Hãy trả lời khách hàng một cách nhiệt tình, ấm áp, gần gũi và chu đáo. "
            "Cung cấp thông tin chính xác về các căn/phòng homestay (bungalow, nhà gỗ, áp mái, villa hồ bơi, glamping), mức giá, dịch vụ tiệc nướng BBQ, bếp tự nấu, thủ tục check-in/check-out và hotline 1900 8899. "
            "Dựa trên dữ liệu homestay được cung cấp dưới đây:\n\n"
            f"=== Dữ liệu StayEasy Homestay ===\n{context}\n\n"
        )

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=MAX_TOKENS,
                    temperature=0.7
                )
                return response.choices[0].message.content

            except Exception as e:
                msg = str(e).lower()
                print(f"⚠️ Lỗi Gemini/OpenAI (attempt {attempt}): {e}")
                if "rate limit" in msg or "tpm" in msg:
                    if attempt < MAX_RETRIES:
                        print(f"⏳ Rate limit – chờ {RETRY_DELAY}s rồi thử lại...")
                        time.sleep(RETRY_DELAY)
                    else:
                        return "⚠️ Trợ lý StayEasy đang nhận quá nhiều yêu cầu. Quý khách vui lòng thử lại sau giây lát."
                else:
                    return "⚠️ Trợ lý StayEasy đang bận. Quý khách vui lòng gọi Hotline 1900 8899 để được hỗ trợ ngay."

        return "⚠️ Không thể kết nối đến trợ lý StayEasy sau nhiều lần thử."

# Alias để tương thích server.py
MedicalChatbot = StayEasyChatbot
