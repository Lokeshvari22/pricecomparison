# utils.py
import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import imagehash
from PIL import Image
from io import BytesIO

SHOP1_URL = 'https://shop-fmsg.vercel.app/'
SHOP2_URL = 'https://shop2-mauve.vercel.app/'

def normalize(text):
    return re.sub(r'[^a-z0-9 ]', '', text.lower()).strip()

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def jaccard_similarity(a, b):
    set_a, set_b = set(normalize(a).split()), set(normalize(b).split())
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union != 0 else 0

def get_image_hash(img_url):
    try:
        response = requests.get(img_url, stream=True, timeout=5)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content)).convert('L').resize((32, 32))
            return imagehash.phash(image)
    except:
        return None

# ------------------------ Scoring Helpers ------------------------

def extract_mobile_features(features_html):
    values = {
        'Processor': 0, 'RAM': 0, 'Storage': 0, 'Display': 0,
        'Battery': 0, 'Camera': 0, 'Build': 0, 'Software': 0,
        'Charging': 0, 'Ecosystem': 0, 'Audio': 0, 'Gaming': 0
    }
    lines = features_html.split('\n')
    for line in lines:
        # Processor scoring
        if 'Processor' in line:
            if 'A17' in line or 'Snapdragon 8 Gen 3' in line:
                values['Processor'] = 25  # Increased for high-end processors
            elif 'Dimensity 9300' in line or 'Exynos 2400' in line:
                values['Processor'] = 20
            else:
                values['Processor'] = 10

        # RAM scoring
        elif 'RAM' in line:
            nums = re.findall(r'\d+', line)
            values['RAM'] = min(int(nums[0]), 24) / 24 * 15 if nums else 0  # Cap raised to 24GB for better scaling

        # Storage scoring
        elif 'Storage' in line:
            nums = re.findall(r'\d+', line)
            values['Storage'] = min(int(nums[0]), 2048) / 2048 * 15 if nums else 0  # Cap raised to 2TB

        # Display scoring
        elif 'Display' in line:
            if 'LTPO' in line or '120Hz' in line or 'AMOLED' in line or 'HDR' in line:
                values['Display'] = 25  # Raised for advanced display features
            else:
                values['Display'] = 15

        # Battery scoring
        elif 'Battery' in line:
            nums = re.findall(r'\d+', line)
            if nums:
                capacity = int(nums[0])
                efficiency_bonus = 3 if 'iOS' in line else 1
                values['Battery'] = (min(capacity, 6000) / 6000 * 18) + efficiency_bonus  # Cap raised to 6000mAh

        # Camera scoring
        elif 'Camera' in line:
            if '108MP' in line or 'Zeiss' in line or 'Photonic Engine' in line:
                values['Camera'] = 25  # Increased for advanced optics
            elif '48MP' in line:
                values['Camera'] = 20
            else:
                values['Camera'] = 10

        # Build scoring
        elif 'Build' in line:
            if 'Titanium' in line or 'Ceramic' in line or 'IP68' in line:
                values['Build'] = 20
            elif 'Gorilla Glass Victus' in line:
                values['Build'] = 15
            else:
                values['Build'] = 10

        # Software scoring
        elif 'OS' in line or 'iOS' in line or 'Android' in line:
            if 'iOS' in line or 'Android 14' in line:
                values['Software'] = 20
            else:
                values['Software'] = 10

        # Charging scoring
        elif 'Charging' in line:
            if 'Fast charging' in line and 'Wireless charging' in line:
                values['Charging'] = 20
            elif 'Reverse charging' in line:
                values['Charging'] = 15
            else:
                values['Charging'] = 10

        # Ecosystem scoring
        elif 'Ecosystem' in line:
            if 'AirDrop' in line or 'Handoff' in line or 'MagSafe' in line:
                values['Ecosystem'] = 20
            elif 'Extended RAM' in line:
                values['Ecosystem'] = 15
            else:
                values['Ecosystem'] = 10

        # Audio scoring
        elif 'Audio' in line:
            if 'Dolby Atmos' in line or 'Stereo speakers' in line:
                values['Audio'] = 15
            else:
                values['Audio'] = 10

        # Gaming scoring
        elif 'Gaming' in line:
            if 'Gaming mode' in line or 'Cooling system' in line:
                values['Gaming'] = 20  # Increased for enhanced gaming features
            else:
                values['Gaming'] = 10

    return values

    """values = {
        'Processor': 0, 'RAM': 0, 'Storage': 0, 'Display': 0,
        'Battery': 0, 'Camera': 0, 'Build': 0, 'Software': 0,
        'Charging': 0, 'Ecosystem': 0, 'Audio': 0, 'Gaming': 0
    }
    lines = features_html.split('\n')
    for line in lines:
        if 'Processor' in line:
            if 'A17' in line or 'Snapdragon 8 Gen 3' in line:
                values['Processor'] = 20
            else:
                values['Processor'] = 10
        elif 'RAM' in line:
            nums = re.findall(r'\d+', line)
            values['RAM'] = min(int(nums[0]), 16) / 16 * 10 if nums else 0
        elif 'Storage' in line:
            nums = re.findall(r'\d+', line)
            values['Storage'] = min(int(nums[0]), 1024) / 1024 * 10 if nums else 0
        elif 'Display' in line:
            if 'LTPO' in line or '120Hz' in line or 'AMOLED' in line:
                values['Display'] = 20
            else:
                values['Display'] = 10
        elif 'Battery' in line:
            nums = re.findall(r'\d+', line)
            if nums:
                capacity = int(nums[0])
                efficiency_bonus = 3 if 'iOS' in line else 1
                values['Battery'] = (min(capacity, 5000) / 5000 * 15) + efficiency_bonus
        elif 'Camera' in line:
            if '48MP' in line or 'Photonic Engine' in line:
                values['Camera'] = 20
            else:
                values['Camera'] = 10
        elif 'Build' in line:
            if 'Titanium' in line or 'IP68' in line:
                values['Build'] = 20
        elif 'OS' in line or 'iOS' in line or 'Android' in line:
            if 'iOS' in line or 'Android 14' in line:
                values['Software'] = 20
            else:
                values['Software'] = 10
        elif 'Charging' in line:
            if 'Fast charging' in line or 'Wireless charging' in line:
                values['Charging'] = 15
            elif 'Reverse charging' in line:
                values['Charging'] = 10
            else:
                values['Charging'] = 5
        elif 'Ecosystem' in line:
            if 'AirDrop' in line or 'Handoff' in line or 'MagSafe' in line:
                values['Ecosystem'] = 15
            else:
                values['Ecosystem'] = 5
        elif 'Audio' in line:
            if 'Dolby Atmos' in line or 'Stereo speakers' in line:
                values['Audio'] = 15
            else:
                values['Audio'] = 5
        elif 'Gaming' in line:
            if 'Gaming mode' in line or 'Cooling system' in line:
                values['Gaming'] = 15
            else:
                values['Gaming'] = 5
    return values"""

def extract_laptop_features(features_html):
    values = {
        'Processor': 0, 'RAM': 0, 'Storage': 0, 'Display': 0,
        'Battery': 0, 'Build': 0, 'Graphics': 0, 'OS': 0, 'Ports': 0
    }
    lines = features_html.lower().split('\n')
    for line in lines:
        # Processor detection
        if 'm2 pro' in line or 'm1 pro' in line:
            values['Processor'] = 20
        elif 'i9' in line or 'ryzen 9' in line:
            values['Processor'] = 20
        elif 'i7' in line or 'ryzen 7' in line:
            values['Processor'] = 15
        elif 'i5' in line or 'ryzen 5' in line:
            values['Processor'] = 10

        # RAM detection
        if '64gb' in line or '32gb' in line:
            values['RAM'] = 20
        elif '16gb' in line:
            values['RAM'] = 15
        elif '8gb' in line:
            values['RAM'] = 10

        # Storage detection
        if '1tb' in line or '2tb' in line:
            values['Storage'] = 20
        elif 'ssd' in line:
            values['Storage'] = 15
        elif 'hdd' in line:
            values['Storage'] = 5

        # Display detection
        if 'retina' in line or 'hdr' in line or 'oled' in line:
            values['Display'] = 20
        elif '144hz' in line or 'ips' in line:
            values['Display'] = 15
        elif '1080p' in line:
            values['Display'] = 10

        # Battery detection
        if '17hr' in line or '20hr' in line:
            values['Battery'] = 15
        elif '12hr' in line or '15hr' in line:
            values['Battery'] = 10
        elif '5hr' in line or '8hr' in line:
            values['Battery'] = 5

        # Build detection
        if 'recycled aluminum' in line or 'titanium' in line:
            values['Build'] = 15
        elif 'metal' in line or 'aluminum' in line:
            values['Build'] = 10
        elif 'plastic' in line:
            values['Build'] = 5

        # Graphics detection
        if 'rtx 40' in line:
            values['Graphics'] = 20
        elif 'rtx' in line:
            values['Graphics'] = 15
        elif 'gtx' in line or 'integrated' in line:
            values['Graphics'] = 10

        # OS detection
        if 'macos ventura' in line or 'windows 11 pro' in line:
            values['OS'] = 15
        elif 'windows 11' in line or 'macos' in line:
            values['OS'] = 10

        # Ports detection
        if 'hdmi 2.1' in line or 'ethernet' in line:
            values['Ports'] = 15
        elif 'thunderbolt' in line or 'usb-c' in line:
            values['Ports'] = 10

    return values
    """values = {
        'Processor': 0, 'RAM': 0, 'Storage': 0, 'Display': 0,
        'Battery': 0, 'Build': 0, 'Graphics': 0, 'OS': 0, 'Ports': 0
    }
    lines = features_html.lower().split('\n')
    for line in lines:
        if 'i9' in line or 'ryzen 9' in line:
            values['Processor'] = 20
        elif 'i7' in line or 'ryzen 7' in line:
            values['Processor'] = 15
        elif 'i5' in line or 'ryzen 5' in line:
            values['Processor'] = 10
        if '16gb' in line:
            values['RAM'] = 15
        elif '8gb' in line:
            values['RAM'] = 10
        elif '32gb' in line:
            values['RAM'] = 20
        if 'ssd' in line:
            values['Storage'] = 15
        elif 'hdd' in line:
            values['Storage'] = 5
        if '144hz' in line or 'oled' in line:
            values['Display'] = 15
        elif 'ips' in line:
            values['Display'] = 10
        if 'battery' in line and ('8hr' in line or '10hr' in line):
            values['Battery'] = 10
        elif 'battery' in line and ('4hr' in line or '5hr' in line):
            values['Battery'] = 5
        if 'metal' in line or 'aluminum' in line:
            values['Build'] = 10
        elif 'plastic' in line:
            values['Build'] = 5
        if 'rtx' in line:
            values['Graphics'] = 15
        elif 'gtx' in line or 'integrated' in line:
            values['Graphics'] = 10
        if 'windows 11' in line or 'macos' in line:
            values['OS'] = 10
        if 'thunderbolt' in line or 'usb-c' in line:
            values['Ports'] = 10
    return values"""

def calculate_specs_score(features_html, category):
    if category == 'mobiles':
        features = extract_mobile_features(features_html)
        weights = {
           'Processor': 0.28, 'RAM': 0.07, 'Storage': 0.07,
           'Display': 0.20, 'Battery': 0.10, 'Camera': 0.28,
           'Build': 0.10, 'Software': 0.10, 'Charging': 0.04,
           'Ecosystem': 0.06, 'Audio': 0.06, 'Gaming': 0.04
        }
        """weights = {
            'Processor': 0.30, 'RAM': 0.05, 'Storage': 0.05,
            'Display': 0.20, 'Battery': 0.10, 'Camera': 0.30,
            'Build': 0.10, 'Software': 0.10, 'Charging': 0.05,
            'Ecosystem': 0.05, 'Audio': 0.05, 'Gaming': 0.05
        }"""
        max_score = 20 * sum(weights.values())
    else:
        features = extract_laptop_features(features_html)
        """weights = {
            'Processor': 0.25, 'RAM': 0.15, 'Storage': 0.10, 'Display': 0.15,
            'Battery': 0.10, 'Build': 0.05, 'Graphics': 0.10, 'OS': 0.05, 'Ports': 0.05
        }"""
        weights = {
            'Processor': 0.25,  # Increased for high-end processors
            'RAM': 0.16,  # Increased slightly
            'Storage': 0.15,  # Increased slightly
            'Display': 0.18,  # Increased for top-tier screens
            'Battery': 0.18,  # Increased for extended battery life
            'Build': 0.10,  # Increased to reflect premium materials
            'Graphics': 0.12,  # Slightly reduced to balance other features
            'OS': 0.08,  # Increased for software optimization
            'Ports': 0.08  # Increased slightly for better connectivity
        }
        max_score = (
            20 * weights['Processor'] + 20 * weights['RAM'] + 15 * weights['Storage'] +
            15 * weights['Display'] + 10 * weights['Battery'] + 10 * weights['Build'] +
            15 * weights['Graphics'] + 10 * weights['OS'] + 10 * weights['Ports']
        )
    raw_score = sum(features.get(key, 0) * weights.get(key, 0) for key in weights)
    return round((raw_score / max_score) * 100, 2)
    
def calculate_sentiment_score(review, min_reviews=5):
    sentiment = TextBlob(review).sentiment.polarity
    return round(sentiment * 100 if len(review.split()) >= min_reviews else 50, 2)

def extract_product_data(url, filter_keyword, category):
    products = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if category == 'clothes':
        for item in soup.find_all('div', class_='pro'):
            name = item.find('h5').text.strip()
            if not all(word in normalize(name) for word in normalize(filter_keyword).split()):
                continue
            price = int(item.find('h4').text.replace('₹', '').strip())
            rating = len(item.find('div', class_='star').find_all('i', class_='ri-star-fill')) + \
                     0.5 * len(item.find('div', class_='star').find_all('i', 'ri-star-half-line'))
            img_url = item.find('img')['src']
            if not img_url.startswith('http'):
                img_url = url.rstrip('/') + '/' + img_url.lstrip('/')
            img_hash = get_image_hash(img_url)
            buy_link = url
            products.append({
                'name': name, 'price': price, 'rating': rating,
                'image': img_url, 'link': buy_link, 'hash': img_hash,
                'features': '', 'reviews': '', 'specs_score': 0,
                'sentiment_score': 0, 'final_score': 0, 'source': url
            })
        return products
    current_brand = None
    for tag in soup.find_all(['h2', 'div']):
        if tag.name == 'h2':
            current_brand = tag.get_text(strip=True).lower()
        
        elif tag.name == 'div' and 'product-card' in tag.get('class', []):
            if not current_brand or filter_keyword.lower() not in current_brand:
                continue

            name_tag = tag.find('h3', class_='product-title')
            name = name_tag.get_text(strip=True) if name_tag else "Unknown"

            # Logic for price and rating extraction
            price_tag = None
            rating_tag = None
            for p in tag.find_all('p'):
                if 'Price:' in p.get_text():
                    price_tag = p
                elif 'Rating:' in p.get_text():
                    rating_tag = p

            price = int(re.sub(r'[^\d]', '', price_tag.get_text())) if price_tag else 0
            rating = float(re.findall(r'[\d.]+', rating_tag.get_text())[0]) if rating_tag else 0

            img_tag = tag.find('img')
            img_url = img_tag['src'] if img_tag else ''
            if not img_url.startswith('http'):
                img_url = url.rsplit('/', 1)[0] + '/' + img_url.lstrip('/')

            buy_tag = tag.find('a', class_='buy-btn')
            buy_url = buy_tag['href'] if buy_tag else url

            feature_ul = tag.find('ul', id=re.compile('features'))
            features_html = feature_ul.get_text(separator='\n').strip() if feature_ul else ''

                         # Handle reviews from multiple paragraphs
            reviews_div = tag.find('div', id=re.compile('reviews'))
            if reviews_div:
                review_text = ' '.join([p.get_text(strip=True) for p in reviews_div.find_all('p')])
            else:
                review_text= "No reviews available"
            specs_score = calculate_specs_score(features_html, category)
            sentiment_score = calculate_sentiment_score(review_text)
            final_score = round((specs_score * 0.7) + (sentiment_score * 0.3), 2)
            products.append({
                'name': name, 'price': price, 'rating': rating,
                'image': img_url, 'link': buy_url,
                'features': features_html, 'reviews': review_text,
                'specs_score': specs_score, 'sentiment_score': sentiment_score,
                'final_score': final_score, 'source': url
             })
    return products

def compare_clothing_products(products1, products2):
    matches = []
    for prod1 in products1:
        best_match = None
        best_score = 0
        for prod2 in products2:
            name_sim = jaccard_similarity(prod1['name'], prod2['name'])
            img_sim = 1 - (prod1['hash'] - prod2['hash']) / len(prod1['hash'].hash) if prod1['hash'] and prod2['hash'] else 0
            score = (name_sim * 0.6) + (img_sim * 0.4)
            if score > best_score:
                best_match, best_score = prod2, score
        if best_match:
            matches.append({ 'prod1': prod1, 'prod2': best_match, 'score': round(best_score, 2) })
    return matches
def extract_products_by_category(shop_url, category, offer_only=False):
    products = []
    current_section = None
    url = f"{shop_url}sproduct.html"

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        for tag in soup.find_all(['h2', 'div']):
            if tag.name == 'h2':
                current_section = tag.get_text(strip=True).lower()
            elif tag.name == 'div' and 'product-card' in tag.get('class', []):
                if current_section and category.lower() in current_section:
                    
                    # Offer filtering
                    price_tag = tag.find('p')
                    has_offer = price_tag and price_tag.find('span')
                    
                    if offer_only and not has_offer:
                        continue
                    
                    name = tag.find('h3', class_='product-title').get_text(strip=True)
                    img_tag = tag.find('img')
                    image = img_tag['src']
                    if image.startswith('/'):
                        image = shop_url.rstrip('/') + image
                    elif not image.startswith('http'):
                        image = shop_url.rstrip('/') + '/' + image
                    rating_tag = tag.find_all('p')[1]
                    rating = rating_tag.get_text(strip=True) if rating_tag else "No rating"
                    source = 'shop1' if 'shop-fmsg' in url else 'shop2'

                    if has_offer:
                        original_price = price_tag.get_text(strip=True).replace(price_tag.find('span').get_text(strip=True), '')
                        discounted_price = price_tag.find('span').get_text(strip=True)
    
                        # Format: original in green (strikethrough), discounted in red
                        price = f'<del style="color: green;">{original_price.strip()}</del> <span style="color: red; font-weight: bold;">{discounted_price}</span>'
                    else:
                        price = f'<span style="color: black;">{price_tag.get_text(strip=True)}</span>'

                    products.append((name, price, url, image, rating, source))
    except Exception as e:
        print(f"[ERROR] extract_products_by_category - {category}: {e}")

    return products