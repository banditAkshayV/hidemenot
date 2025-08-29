#!/usr/bin/env python3
"""
Test script for the new crash flow in hidemenot
"""

import requests
import time

def test_crash_flow():
    """Test the complete crash flow"""
    base_url = 'http://localhost:5000'
    session = requests.Session()
    
    print("🧪 Testing hidemenot crash flow...")
    print("=" * 50)
    
    # Step 1: Register and login
    print("1️⃣ Registering and logging in...")
    
    register_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = session.post(f'{base_url}/register', data=register_data)
    print(f"   Register response: {response.status_code}")
    
    login_data = {
        'username': 'testuser', 
        'password': 'testpass123'
    }
    
    response = session.post(f'{base_url}/login', data=login_data)
    print(f"   Login response: {response.status_code}")
    
    # Step 2: Check homepage before crash (should show demo.png, no crash comment)
    print("\n2️⃣ Checking homepage before crash...")
    response = session.get(f'{base_url}/')
    
    if 'demo.png' in response.text:
        print("   ✅ Homepage shows demo.png")
    else:
        print("   ❌ Homepage not showing demo.png")
    
    if 'crash_image_url' in response.text:
        print("   ❌ Crash comment visible (shouldn't be)")
    else:
        print("   ✅ No crash comment visible")
    
    # Step 3: Upload polyglot file to trigger crash
    print("\n3️⃣ Uploading polyglot file to trigger crash...")
    
    with open('minimal_polyglot.png', 'rb') as f:
        files = {
            'image': ('polyglot.png', f, 'image/png')
        }
        data = {
            'message': 'test crash message'
        }
        
        response = session.post(f'{base_url}/encode', files=files, data=data, allow_redirects=False)
        print(f"   Upload response: {response.status_code}")
        
        if response.status_code == 500:
            print("   ✅ Got 500 error as expected")
        else:
            print(f"   ❌ Expected 500, got {response.status_code}")
    
    # Step 4: Follow the redirect chain (500 page -> homepage)
    print("\n4️⃣ Testing redirect from 500 page...")
    
    # Simulate visiting 500 page then homepage
    response = session.get(f'{base_url}/?from_crash=true')
    
    if 'democrashed.png' in response.text:
        print("   ✅ Homepage now shows democrashed.png")
    else:
        print("   ❌ Homepage not showing democrashed.png")
        print("   Response contains:", 'demo.png' if 'demo.png' in response.text else 'unknown image')
    
    if 'crash_image_url: /static/uploads/democrashed.png' in response.text:
        print("   ✅ Crash comment now visible with correct URL")
    else:
        print("   ❌ Crash comment not visible or wrong URL")
    
    # Step 5: Check if democrashed.png file was created
    print("\n5️⃣ Checking if crash image file was created...")
    
    response = session.get(f'{base_url}/static/uploads/democrashed.png')
    
    if response.status_code == 200:
        print("   ✅ democrashed.png file exists and accessible")
        print(f"   File size: {len(response.content)} bytes")
    else:
        print("   ❌ democrashed.png file not found")
    
    # Step 6: Test alternative decoder
    print("\n6️⃣ Testing alternative decoder...")
    
    response = session.get(f'{base_url}/decode-alternative')
    
    if response.status_code == 200:
        try:
            data = response.json()
            if 'message' in data and data['message']:
                print("   ✅ Alternative decoder working")
                print(f"   Decoded message: {data['message'][:50]}...")
            else:
                print("   ❌ Alternative decoder returned empty message")
        except:
            print("   ❌ Alternative decoder response not valid JSON")
    else:
        print(f"   ❌ Alternative decoder failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_crash_flow()
