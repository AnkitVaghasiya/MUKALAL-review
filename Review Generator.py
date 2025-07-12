import random
from pytrends.request import TrendReq

# --- Optional Paraphrasing for English Reviews ---
try:
    from transformers import pipeline
    paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")
    paraphrasing_enabled = True
except Exception:
    paraphrasing_enabled = False
    paraphraser = None

# --- Get Trending Keywords ---
pytrends = TrendReq(hl='en-US', tz=330)
kw_list = ["ethnic wear wholesaler", "bulk kurti supplier", "wholesale ladies dress", "bulk ethnic wear", "ethnic wear manufacturer"]
try:
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='IN', gprop='')
    trending = pytrends.related_queries()
except Exception:
    trending = {}

seo_keywords = set()
for kw in kw_list:
    if kw in trending and 'top' in trending[kw] and trending[kw]['top'] is not None:
        try:
            top_df = trending[kw]['top']
            for row in top_df.to_dict('records'):
                if 'query' in row:
                    cleaned = row['query'].replace(" ", "").replace("-", "")
                    seo_keywords.add(cleaned)
        except Exception:
            pass

if not seo_keywords:
    seo_keywords = set(["Wholesale Ethnic Wear", "Bulk Kurti Supplier", "Ladies Dress Manufacturer", "Surat Ethnic Hub", "Bulk Gown Dealer"])

seo_keywords = list(seo_keywords)

# --- Review Parts ---
products = ["Kurti", "Tunic", "Co-ord Set", "Pant Pair", "Palazzo Pair", "Aliya Pair", "Crop Top", "Gown"]
postfix = {"gu": "lidha", "hi": "liye"}  # Men buyers

areas = ["Surat", "Varachha", "Laxman Nagar"]
emojis = ["📦", "💼", "🔥", "🧵", "✅", "🛍️", "💰", "🧳", "💯"]

starters_en = ["", "Great deal,", "Fast dispatch,", "From my experience,", "To all resellers,", "Honest opinion,", "No complaints,", "Highly impressed,"]
enders_en = ["", "Already reordered!", "Must try for resellers.", "Perfect for margin.", "Ideal for online sellers.", "Bulk buyers must visit.", "Thank you team!", "Trusted source.", "Profit guaranteed!"]
mid_phrases_en = ["bulk rates are best", "quality is consistent", "fabric is export-level", "delivery was on time", "range is vast", "stitching is clean", "resellers will profit", "MOQ is reasonable", "packaging was perfect"]

starters_hi = ["", "Bhai,", "Main reseller hoon,", "Experience share kar raha hoon,", "Bulk me liya tha,", "Direct manufacturer se,", "Delivery quick thi,"]
enders_hi = ["", "Dubara order pakka.", "Paise vasool deal.", "High margin milta hai.", "Perfect for resale.", "Trusted supplier.", "Main sabko recommend karunga.", "Offline sell ke liye perfect hai."]
mid_phrases_hi = ["bulk price best he", "fabric export quality ka he", "fitting ekdum perfect", "range bohot achhi he", "delivery time pe aayi", "packaging secure tha", "margin achha mila", "MOQ bhi kam he", "seller support bhi mila"]

starters_gu = ["", "Maja aavi,", "Wholesale ma lidhu che,", "Dealers ne suggest karish,", "Reseller mate ekdam perfect,", "Direct factory mathi,", "On time delivery che,"]
enders_gu = ["", "Pachhi pan order karish.", "Biji baar confirm order.", "Paise vasool che.", "Margin saras che.", "Fast delivery.", "Kharekhar vishwasniya che.", "Resell mate best che."]
mid_phrases_gu = ["bhav to sasto j che", "kapdu export quality nu che", "delivery samay par avi", "packaging saru che", "MOQ saru che", "range khubaj moti che", "margin made che", "collection updated che", "staff helpful che"]

# --- Generate One Review ---
def generate_review(lang, product, area, emoji, keyword):
    shop_name = "MUKALAL"
    post = postfix.get(lang, "")

    seo_line = random.choice([
        f"Best wholesale {product.lower()} supplier in {area}.",
        f"Top-rated ethnic wear manufacturer in {area}.",
        f"{shop_name} is trusted for bulk {product.lower()} deals.",
        f"Buy ethnic wear in bulk from {shop_name}.",
    ])

    if lang == "en":
        starter = random.choice(starters_en)
        ender = random.choice(enders_en)
        mid = random.choice(mid_phrases_en)
        review = random.choice([
            f"{starter} Bought {product}s in bulk from {shop_name}, {mid}, {emoji} best for {keyword}. {ender}",
            f"{starter} {shop_name} in {area} gave me {product}s at great rates – {mid}. {emoji} {ender}",
            f"{starter} My order of {product}s was smooth from {shop_name}, {mid}, worth every rupee. {emoji} {ender}"
        ])
    elif lang == "hi":
        starter = random.choice(starters_hi)
        ender = random.choice(enders_hi)
        mid = random.choice(mid_phrases_hi)
        review = random.choice([
            f"{starter} {shop_name} ({area}) se {product} {post} bulk me liya, {mid}. {emoji} {ender}",
            f"{starter} {product} {post} direct factory se mila, {mid}, resale ke liye perfect. {emoji} {ender}"
        ])
    elif lang == "gu":
        starter = random.choice(starters_gu)
        ender = random.choice(enders_gu)
        mid = random.choice(mid_phrases_gu)
        review = random.choice([
            f"{starter} {area} mathi {product} {post} bulk ma lidhu from {shop_name}, {mid}. {emoji} {ender}",
            f"{starter} {shop_name} {area} ma wholesaler che, {product} {post} perfect quality. {emoji} {ender}"
        ])

    # Keep SEO line in English regardless of language
    if random.random() < 0.5:
        return f"{seo_line} {review}".strip()
    else:
        return f"{review} {seo_line}".strip()

# --- Generate All Reviews ---
reviews_set = set()
N = 500
while len(reviews_set) < N:
    lang = random.choice(["hi", "gu", "en"])
    product = random.choice(products)
    area = random.choice(areas)
    emoji = random.choice(emojis) if random.random() > 0.2 else ""
    keyword = random.choice(seo_keywords)
    review = generate_review(lang, product, area, emoji, keyword)

    if lang == "en" and paraphrasing_enabled and random.random() > 0.5:
        try:
            review = paraphraser(review, max_length=60, num_return_sequences=1)[0]['generated_text']
        except:
            pass

    reviews_set.add(review)

# --- Save to reviews.js ---
with open("reviews.js", "w", encoding="utf-8") as f:
    f.write("const reviews = [\n")
    for r in sorted(reviews_set):
        escaped = r.replace('"', '\\"')
        f.write(f'"{escaped}",\n')
    f.write("];\n")

print(f"✅ Generated {len(reviews_set)} wholesale-focused SEO reviews and saved to reviews.js")
# --- End of Code ---