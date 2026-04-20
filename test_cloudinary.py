import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dvuooxbqi",
    api_key="875143959481713",
    api_secret="BsLyRtEvfVCEZOdQ6JWnY6mTEqI",
    secure=True
)

# Test upload with a sample image
try:
    result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/sample.jpg")
    print("✅ Cloudinary connection successful!")
    print(f"Uploaded to: {result['secure_url']}")
except Exception as e:
    print(f"❌ Cloudinary connection failed: {e}")