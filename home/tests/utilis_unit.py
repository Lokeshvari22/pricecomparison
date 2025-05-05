from home.utils import (
    calculate_sentiment_score,
    calculate_specs_score,
    jaccard_similarity,
    compare_clothing_products
)
import imagehash
from PIL import Image
import numpy as np

def test_sentiment_positive():
    review = "Amazing battery life and smooth performance with excellent display."
    score = calculate_sentiment_score(review)
    print(f"Positive sentiment score: {score}")
    assert score > 50

def test_sentiment_negative():
    review = "The worst camera and battery performance I have ever experienced."
    score = calculate_sentiment_score(review)
    print(f"Negative sentiment score: {score}")
    assert score < 50

def test_specs_score_mobile():
    html = """Processor: Snapdragon 8 Gen 3
RAM: 8GB
Storage: 256GB
Display: 120Hz AMOLED HDR10+
Battery: 5000mAh
Camera: 48MP
Build: Titanium
Software: Android 14
Charging: Fast charging and Wireless charging
Ecosystem: Extended Ram
Audio: Stereo speakers with Dolby Atmos
Gaming: Cooling system"""
    score = calculate_specs_score(html, "mobiles")
    print(f"Mobile specs score: {score}")
    assert score > 70

def test_name_similarity():
    sim = jaccard_similarity("iPhone 14 Pro", "iPhone 14 Pro Max")
    print(f"Jaccard similarity: {sim}")
    assert sim > 0.5

def test_compare_products():
    img = Image.fromarray(np.random.randint(0, 255, (32, 32), dtype=np.uint8))
    hash1 = imagehash.average_hash(img)
    hash2 = imagehash.average_hash(img)

    p1 = {'name': 'Jacket', 'hash': hash1}
    p2 = {'name': 'Jacket', 'hash': hash2}

    matches = compare_clothing_products([p1], [p2])
    print(f"Matched products count: {len(matches)}")
    assert len(matches) == 1
