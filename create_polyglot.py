#!/usr/bin/env python3
"""
Polyglot Image Generator for hidemenot Challenge

This script creates test polyglot files that trigger the server crash mechanism.
A polyglot file has the magic bytes of one format but contains markers of another.
"""

import os

def create_png_jpeg_polyglot():
    """Create a PNG file with JPEG markers (polyglot)"""
    filename = 'test_polyglot_png.png'
    
    with open(filename, 'wb') as f:
        # PNG magic bytes
        f.write(b'\x89PNG\r\n\x1a\n')
        
        # Add some PNG-like structure
        f.write(b'\x00\x00\x00\rIHDR')
        f.write(b'\x00' * 13)  # IHDR data
        
        # Insert JPEG marker to make it a polyglot
        f.write(b'JFIF\x00\x01\x01\x01')
        
        # Add more data to make it look like a real file
        f.write(b'\x00' * 200)
        
    print(f"Created {filename} - PNG with JPEG markers")
    return filename

def create_jpeg_png_polyglot():
    """Create a JPEG file with PNG markers (polyglot)"""
    filename = 'test_polyglot_jpeg.jpg'
    
    with open(filename, 'wb') as f:
        # JPEG magic bytes
        f.write(b'\xff\xd8\xff\xe0')
        
        # JFIF header
        f.write(b'\x00\x10JFIF\x00\x01\x01\x01')
        
        # Insert PNG marker to make it a polyglot
        f.write(b'\x89PNG\r\n\x1a\n')
        
        # Add more JPEG-like data
        f.write(b'\xff\xd9')  # End of image marker
        f.write(b'\x00' * 150)
        
    print(f"Created {filename} - JPEG with PNG markers")
    return filename

def create_minimal_polyglot():
    """Create minimal polyglot for testing"""
    filename = 'minimal_polyglot.png'
    
    with open(filename, 'wb') as f:
        # PNG signature
        f.write(b'\x89PNG\r\n\x1a\n')
        
        # Minimal PNG structure with JPEG content
        f.write(b'\x00\x00\x00\x0dIHDR')  # PNG header chunk
        f.write(b'\x00\x00\x00\x01')      # Width: 1
        f.write(b'\x00\x00\x00\x01')      # Height: 1
        f.write(b'\x08\x02\x00\x00\x00')  # Bit depth, color type, etc.
        f.write(b'\x90wS\xde')            # CRC
        
        # Add JPEG marker that shouldn't be in PNG
        f.write(b'JFIF\x00\x01')
        
        # End PNG properly
        f.write(b'\x00\x00\x00\x00IEND\xaeB`\x82')
        
    print(f"Created {filename} - Minimal PNG/JPEG polyglot")
    return filename

def main():
    """Create all test polyglot files"""
    print("🔧 Creating test polyglot files for hidemenot challenge...")
    print("=" * 60)
    
    files_created = []
    
    try:
        # Create different types of polyglots
        files_created.append(create_png_jpeg_polyglot())
        files_created.append(create_jpeg_png_polyglot())
        files_created.append(create_minimal_polyglot())
        
        print("\n✅ Successfully created polyglot files!")
        print("\n📋 Usage Instructions:")
        print("1. Start the hidemenot application (python app.py)")
        print("2. Register and login to the web application")
        print("3. Go to the Encode page")
        print("4. Upload one of these polyglot files:")
        
        for i, filename in enumerate(files_created, 1):
            file_size = os.path.getsize(filename)
            print(f"   {i}. {filename} ({file_size} bytes)")
        
        print("\n🎯 Expected Results:")
        print("- Server will detect the magic byte mismatch")
        print("- You'll be redirected back to homepage with error message")
        print("- Demo image on homepage will change to crash image")
        print("- Check page source for hidden crash_image_url comment")
        
        print("\n⚠️  Note: These files are designed to trigger the crash mechanism")
        print("   and are not valid image files for normal use.")
        
    except Exception as e:
        print(f"❌ Error creating polyglot files: {e}")

if __name__ == "__main__":
    main()
