import os

import dotenv

dotenv.load_dotenv()

# Load environment variables
CONFIG = {
    'MAX_DRIVERS': int(os.getenv("MAX_DRIVERS") or 1),
    'OPENAI_API_KEY': os.getenv("OPENAI_API_KEY")
}
