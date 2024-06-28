from openai import OpenAI

from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product

client = OpenAI(api_key="sk-proj-s7WyfYnogKGcT6Ty30DDT3BlbkFJmn11EtBLGWsK5jAgWjEW")

ASSISTANT_INSTR = ("You are an helpful assistant which helps me to identify clothing. I have the title of "
                   "multiple websites which sell that specific piece of clothing I am looking for. Please "
                   "extract the producer and model of the item based of the title of the websites I found. "
                   "Do not extract size information or other irrelevant details, just the model name!"
                   "If multiple producers or models were mentioned, return the one that is most mentioned "
                   "and makes the most sense. Answer in the pattern:"
                   "\n\nproducer: \"Producer\"\nmodel: \"Model\"")

EXAMPLE_TITLES = ("Patagonia P-6 Logo Responsibili Long sleeve (black 2)\nPatagonia Bicycle T-Shirts for Men | "
                  "Mercari\nเสื้อpatagoniaแท้ ราคาพิเศษ | ซื้อออนไลน์ที่ Shopee ส่งฟรี*ทั่วไทย!\nPolera Manga "
                  "Larga Patagonia | MercadoLibre 📦\nNone\nNone\nMen’s size S Patagonia shirt. Never worn. - "
                  "Depop\nPatagonia | Shirts | Patagonia Long Sleeve Black T Shirt Mens Size S | "
                  "Poshmark\nPatagonia Loong Sleeve\nPositive.cnx | Patagonia Sz. อก 22' ยาว 28' สภาพใหม่ "
                  "ไม่มีตำหนิ สภาพ9/10 ♦️Soldout♦️ Dm:po... | Instagram\n1点限り❣️ Patagonia パタゴニア 長袖 Tシャツ トップス"
                  " ブラック 黒 L パタゴニア トップス - axiomaenergiasolar.com\n[美品]パタゴニア　patagonia ロンT 黒 by "
                  "メルカリ\nPatagonia Men's P-6 Logo Long-Sleeve Responsibili-Tee | "
                  "Patagonia long sleeve, Tees, Patagonia")


class ModelProducerProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        inputs = [li.get_dict_str_str() for li in input_value.get_list()]
        model_producer = _get_producer_model(inputs)
        return Product(model_producer), True  # type: ignore


def _get_producer_model(items: list[dict[str, str | None]]) -> dict[str, str]:
    titles = [item['title'] for item in items if item['title']]
    input_text = "\n".join(titles)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": ASSISTANT_INSTR
            },
            {
                "role": "user",
                "content": EXAMPLE_TITLES
            },
            {
                "role": "assistant",
                "content": "producer: Patagonia\nmodel: Patagonia Men's Long-Sleeved P-6 Logo Responsibili-Tee"
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse the response to extract the producer and model
    response_text = response.choices[0].message.content
    if response_text:
        lines = response_text.strip().split("\n")
        producer = lines[0].split(": ")[1].strip('\"')
        model = lines[1].split(": ")[1].strip('\"')

        return {"producer": producer, "model": model}
    else:
        raise Exception("No response from AI model!")
