import os
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

os.makedirs('media/blog_defaults', exist_ok=True)
urls = [
    "https://images.unsplash.com/photo-1517130038641-a774d04afb3c?q=80&w=600&auto=format&fit=crop", # Gymnastics rings
    "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop", # Gym focus
    "https://images.unsplash.com/photo-1599058945522-28d584b6f4ff?q=80&w=600&auto=format&fit=crop", # Working out
    "https://images.unsplash.com/photo-1526506114842-1e6c459b1e66?q=80&w=600&auto=format&fit=crop", # Athletic stretching
    "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=600&auto=format&fit=crop"  # Strength
]

req = urllib.request.build_opener()
req.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
urllib.request.install_opener(req)

for i, url in enumerate(urls):
    try:
        urllib.request.urlretrieve(url, f"media/blog_defaults/{i+1}.webp")
        print(f"Downloaded {i+1}")
    except Exception as e:
        print(f"Failed {i+1}: {e}")
print("Done")
