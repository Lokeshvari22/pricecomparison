import pytest
from PIL import Image
import imagehash
import numpy as np
from textblob import TextBlob

from home.utils import (
    compare_clothing_products,
    calculate_specs_score,
    calculate_sentiment_score,
)

def test_compare_clothing_products_returns_matches():
    # Use the same image for both products to ensure hash similarity is 1
    img = Image.fromarray(np.ones((64, 64), dtype=np.uint8) * 128)  # Gray image
    hash1 = imagehash.average_hash(img)
    hash2 = imagehash.average_hash(img)

    prod1 = {'name': 'Red T-shirt', 'hash': hash1, 'price': 499, 'site': 'Shop1'}
    prod2 = {'name': 'Red T-shirt', 'hash': hash2, 'price': 500, 'site': 'Shop2'}

    matches = compare_clothing_products([prod1], [prod2])
    assert isinstance(matches, list)
    assert len(matches) > 0
    assert 'prod1' in matches[0]
    assert 'prod2' in matches[0]
    assert 'score' in matches[0]

def test_calculate_specs_score_mobiles():
    features_html = '''
    Processor: Octa Core
    RAM: 8 GB
    Storage: 128 GB
    Display: AMOLED
    Battery: 5000 mAh
    Camera: 64 MP
    Build: Glass
    Software: Android 13
    Charging: Fast Charging
    Ecosystem: Good
    Audio: Stereo
    Gaming: Smooth
    '''
    score = calculate_specs_score(features_html, category='mobiles')
    assert isinstance(score, float)
    assert 0 <= score <= 100

def test_calculate_specs_score_laptops():
    features_html = '''
    Processor: Intel i7
    RAM: 16 GB
    Storage: SSD 512 GB
    Display: IPS Full HD
    Battery: 8 hours
    Build: Aluminium
    Graphics: RTX 3060
    OS: Windows 11
    Ports: USB-C, HDMI
    '''
    score = calculate_specs_score(features_html, category='laptops')
    assert isinstance(score, float)
    assert 0 <= score <= 100

def test_calculate_sentiment_score_high_sentiment():
    review = "This product is absolutely amazing. Loved every feature. Totally worth the money!"
    score = calculate_sentiment_score(review)
    assert isinstance(score, float)
    assert 0 <= score <= 100
    assert score > 50  # Should be more positive

def test_calculate_sentiment_score_few_words_defaults_to_50():
    review = "Nice product"
    score = calculate_sentiment_score(review)
    assert score == 50.0
