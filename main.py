import os
import random
import requests
import json
import cloudinary
from cloudinary.search import Search
import cloudinary.uploader

# ==========================================
# 1. ENVIRONMENT VARIABLES (SECRETS) SETUP
# ==========================================
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "auto_videos") # Default folder name

# Check karna ki saare secrets set hain ya nahi
missing_secrets = []
for secret_name, secret_val in [("WEBHOOK_URL", WEBHOOK_URL), ("CLOUDINARY_CLOUD_NAME", CLOUDINARY_CLOUD_NAME), 
                                ("CLOUDINARY_API_KEY", CLOUDINARY_API_KEY), ("CLOUDINARY_API_SECRET", CLOUDINARY_API_SECRET)]:
    if not secret_val:
        missing_secrets.append(secret_name)

if missing_secrets:
    print(f"❌ Error: Yeh secrets set nahi hain: {', '.join(missing_secrets)}")
    exit(1)

# ==========================================
# 2. CLOUDINARY CONFIGURATION
# ==========================================
cloudinary.config(
  cloud_name = CLOUDINARY_CLOUD_NAME,
  api_key = CLOUDINARY_API_KEY,
  api_secret = CLOUDINARY_API_SECRET,
  secure = True
)

# ==========================================
# 3. HISTORY FILE (Log maintain karne ke liye)
# ==========================================
HISTORY_FILE = "history.txt"
if not os.path.exists(HISTORY_FILE):
    open(HISTORY_FILE, 'w').close()

with open(HISTORY_FILE, 'r') as f:
    posted_videos = f.read().splitlines()

# ==========================================
# 4. FETCH AND SELECT VIDEO FROM CLOUDINARY
# ==========================================
print(f"🔍 Fetching videos from Cloudinary folder: '{CLOUDINARY_FOLDER}'...")
try:
    result = Search()\
        .expression(f'resource_type:video AND folder:{CLOUDINARY_FOLDER}')\
        .sort_by('created_at', 'asc')\
        .max_results(500)\
        .execute()
    
    all_videos = result.get('resources', [])
except Exception as e:
    print(f"❌ Cloudinary se fetch karne mein error: {e}")
    exit(1)

if not all_videos:
    print(f"❌ Cloudinary folder '{CLOUDINARY_FOLDER}' mein koi video nahi mila!")
    exit(1)

# Filter karna (jo history mein nahi hain)
available_videos = [v for v in all_videos if v['public_id'] not in posted_videos]

if not available_videos:
    print("❌ Saare videos post ho chuke hain! Cloudinary mein naye videos daalein.")
    exit(1)

# Pehla available video select karna
selected_video = available_videos[0]
video_id = selected_video['public_id']
video_url = selected_video['secure_url'] 
video_name = selected_video['filename']

print(f"🎬 Video Selected: {video_name} (ID: {video_id})")

# ==========================================
# 5. CONTENT GENERATION (Titles, Captions, Hashtags)
# ==========================================
titles = [
    "Wait for the end! 🤯", "You won't believe this transformation! 🚀", "Then vs. Now ✨", 
    "The ultimate glow up! 🔥", "This is so satisfying to watch! 😍", "Evolution at its finest! 🧬", 
    "Time travel is real! ⏱️", "Old to Modern in seconds! ⏳", "How it started vs How it's going 📈", 
    "Wait for the modern look! 👀", "Mind = Blown 🤯", "This upgrade is insane! 💯", 
    "Nostalgia warning! ⚠️", "The perfect transition does not exi... 🤩", "Upgrading history! 🏛️", 
    "Classic meets contemporary 🥂", "A masterpiece then and now 🎨", "From vintage to visionary 🌟", 
    "Leveling up! ⬆️", "This changed everything 🌍", "You need to see this! 👀", 
    "Blast from the past 🚀", "The ultimate before and after 🔄", "Rewriting history! ✍️", 
    "The modern touch ✨", "Can you believe this? 😲", "Out with the old, in with the new 🗑️➡️🆕", 
    "Bringing the past to the future 🛸", "Wait for the glow up! 💫", "This will make your day! ☀️", 
    "Redesigning the classics 🛠️", "Nothing beats this transformation 🏆", "From basic to breathtaking 💎", 
    "The craziest evolution! 🐒➡️🧍", "This is just pure magic 🪄", "Vintage vibes, modern tech 💻", 
    "Gen Z won't understand this 😂", "What a difference time makes 🕰️", "Unlocking the modern version 🔓", 
    "This hit right in the feels ❤️", "Taking a trip down memory lane 🛣️", "A century of change 💯", 
    "The best glow-up on the internet 🌐", "History reimagined 💭", "Respect the roots 🌳", 
    "This is surprisingly satisfying 😌", "Just wait for the beat drop 🎵", "The upgrade we all needed 🙌", 
    "Pure perfection! 🤌", "Timeless classics upgraded 🕰️✨"
]

captions = [
    "Drop a ❤️ if you love this! Let me know your thoughts in the comments! 👇", 
    "This transition is everything! ✨ What do you guys think?", 
    "Respect the past, embrace the future. 🚀 Tag a friend who needs to see this!", 
    "The glow up is REAL. Rate this transformation from 1-10! 📈", 
    "Which era do you prefer? The old or the modern? Let's debate! 🗣️", 
    "Some things just get better with time. ⏳ Do you agree?", 
    "Nostalgia hits hard! 🥹 Share this with someone who remembers the original.", 
    "Level up complete! 🎮 Hit follow for more epic transformations.", 
    "Proof that evolution is beautiful. 🦋 Leave a comment below!", 
    "They don’t make them like they used to, they make them better! 🔥", 
    "I can't stop watching this loop! 🔁 Double tap if you feel the same.", 
    "Old soul, modern execution. 🛠️ Save this post for later!", 
    "Taking a trip down memory lane before jumping into the future. 🚀", 
    "Goodbye old friend, hello new era. 👋✨", 
    "The past walked so the future could run. 🏃‍♂️💨", 
    "Sometimes a little modern touch is all a classic needs. 🤌", 
    "It took decades of innovation to get here. Worth the wait? 💯", 
    "I still remember when the old version was considered cutting-edge! 😂", 
    "Bringing history into the 21st century! 🏛️➡️🏙️", 
    "A masterpiece then, a masterpiece now. 🎨 Tag a history lover!", 
    "We loved it back then, but we are obsessed with it now! 😍", 
    "Upgrading isn't just about changing; it's about evolving. 🌱", 
    "Keeping the soul, changing the shell. 🐚 Thoughts?", 
    "What a difference time makes. 🕰️ Comment your favorite part!", 
    "This is surprisingly satisfying to watch. 😌 Hit the like button!", 
    "The beauty of evolution captured in one video. 📹 Share with a friend!", 
    "From retro to futuristic in seconds. 🛸 Drop a 💯 if you love this.", 
    "The ultimate before and after. 🔄 Follow for daily content like this!", 
    "Wait for the modern look! 👀 Did we nail it?", 
    "Time travel activated. ⏱️ Where would you go if you had a time machine?", 
    "Breathing new life into the past. 🌬️ Leave your thoughts below!", 
    "The craziest glow-up you'll see today! 🤯 Don't forget to save!", 
    "Vintage engineering vs modern marvels. ⚙️ Which wins?", 
    "The art of transformation. 🎭 Rate this out of 100!", 
    "Remaking the classics for the new generation. 👶👨‍🦳", 
    "How did we survive with the old one? 😂 Tell me in the comments!", 
    "Gen Z will never understand the before. 👶 Tag a millennial!", 
    "The ultimate upgrade. 🆙 Hit subscribe/follow for more!", 
    "You won't believe how this used to look! 😲 Double tap!", 
    "Simply iconic. 👑 Share this on your story!", 
    "Evolution at its finest. 🧬 Tag someone who needs a glow-up!", 
    "Wait for the transition... 🔥 So smooth! Let me know your thoughts.", 
    "History rewritten. ✍️ Do you prefer the original?", 
    "Out with the old, in with the new. 🗑️✨ What do you think?", 
    "Can we get 1000 likes for this epic glow-up? ❤️", 
    "Tell us your favorite part of the modern version below! ⬇️", 
    "Watch till the end to see the final reveal! 🎬", 
    "Share this with a friend who loves vintage aesthetics! 🤝", 
    "Just wow! 🤩 Leave a comment if you watched it more than once.", 
    "The modern-day renaissance. 🏛️ Drop your reactions below!"
]

hashtags = {
    "facebook": "#Viral #Trending #Nostalgia #Makeover #FBReels #VideoOfTheDay #Transformation #ThenAndNow #BeforeAndAfter",
    "instagram": "#ReelsInstagram #GlowUp #ExplorePage #TrendingReels #InstaDaily #VintageVsModern #Aesthetic #MakeoverMagic",
    "youtube": "#Shorts #YouTubeShorts #Trending #ViralVideo #TransformationShorts #Evolution #BeforeAndAfter #Satisfying"
}

# ==========================================
# 6. WEBHOOK PAYLOAD CREATION
# ==========================================
payload = {
    "video_name": video_name,
    "video_url": video_url,
    "title": random.choice(titles),
    "caption": random.choice(captions),
    "hashtags_facebook": hashtags['facebook'],
    "hashtags_instagram": hashtags['instagram'],
    "hashtags_youtube": hashtags['youtube']
}

# ==========================================
# 7. SEND TO WEBHOOK & AUTO-DELETE LOGIC
# ==========================================
print("🚀 Sending data to Webhook...")

try:
    # 1. Webhook ko data bhejna
    response = requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    
    print("✅ Success! Data webhook par chala gaya.")
    
    # 2. Webhook Success hone par Cloudinary se delete karna
    print(f"🗑️ Deleting video '{video_id}' from Cloudinary to save space...")
    delete_response = cloudinary.uploader.destroy(video_id, resource_type="video")
    
    if delete_response.get('result') == 'ok':
        print(f"✅ Video Cloudinary se successfully delete ho gaya!")
    else:
        print(f"⚠️ Warning: Video post ho gaya par Cloudinary se delete nahi hua. Reason: {delete_response}")
    
    # 3. Local History update karna (Log maintain karne ke liye)
    with open(HISTORY_FILE, 'a') as f:
        f.write(video_id + '\n')
    print(f"📝 Local History update ho gayi.")

except requests.exceptions.RequestException as e:
    # Agar webhook fail hua, toh delete wala code run nahi hoga
    print(f"❌ Webhook fail ho gaya: {e}. Video Cloudinary se delete nahi kiya gaya taaki data loss na ho.")
    exit(1)
