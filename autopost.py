import os
import random
import requests
import json
import urllib.parse

# 1. Environment Variables uthana (Webhook URL aur GitHub details)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY") # GitHub Actions automatically yeh deta hai (e.g., username/repo)
GITHUB_BRANCH = os.getenv("GITHUB_REF_NAME", "main") # Current branch (mostly 'main')

if not WEBHOOK_URL:
    print("❌ Error: WEBHOOK_URL secret GitHub mein set nahi hai!")
    exit(1)

# Folders aur Files
VIDEO_DIR = "video"
HISTORY_FILE = "history.txt"

# Check karna ki video folder hai ya nahi
if not os.path.exists(VIDEO_DIR):
    print(f"❌ Error: '{VIDEO_DIR}' folder nahi mila. Kripya video folder banayein.")
    exit(1)

# Agar history.txt nahi hai, toh automatically bana dega
if not os.path.exists(HISTORY_FILE):
    open(HISTORY_FILE, 'w').close()

# 2. History read karna taaki video repeat na ho
with open(HISTORY_FILE, 'r') as f:
    posted_videos = f.read().splitlines()

# Saare videos nikalna (jo .mp4 format mein hain)
all_videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]

# Filter karna jo post nahi hue hain
available_videos = [v for v in all_videos if v not in posted_videos]

if not available_videos:
    print("❌ Saare videos post ho chuke hain! Naye videos daalein ya history.txt clear karein.")
    exit(1)

# 3. Naya video select karna
selected_video = available_videos[0]

# 🔗 4. VIDEO URL GENERATE KARNA (GitHub Raw Link)
# Space ya special characters ko encode karna taaki link break na ho
encoded_video_name = urllib.parse.quote(selected_video)

if GITHUB_REPO:
    video_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/refs/heads/{GITHUB_BRANCH}/{VIDEO_DIR}/{encoded_video_name}"
else:
    # Agar local PC pe test kar rahe ho toh yeh aayega
    video_url = f"https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/{VIDEO_DIR}/{encoded_video_name}"

# 5. 50+ Universal Titles
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

# 6. 50+ Universal Captions
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

# 7. Platform Specific Hashtags
hashtags = {
    "facebook": "#Viral #Trending #Nostalgia #Makeover #FBReels #VideoOfTheDay #Transformation #ThenAndNow #BeforeAndAfter",
    "instagram": "#ReelsInstagram #GlowUp #ExplorePage #TrendingReels #InstaDaily #VintageVsModern #Aesthetic #MakeoverMagic",
    "youtube": "#Shorts #YouTubeShorts #Trending #ViralVideo #TransformationShorts #Evolution #BeforeAndAfter #Satisfying"
}

# 8. Webhook ke liye JSON Payload tayyar karna
payload = {
    "video_name": selected_video,
    "video_url": video_url,  # <-- YEH RAHA AAPKA NAYA VIDEO URL LOGIC
    "title": random.choice(titles),
    "caption": random.choice(captions),
    "hashtags_facebook": hashtags['facebook'],
    "hashtags_instagram": hashtags['instagram'],
    "hashtags_youtube": hashtags['youtube']
}

print(f"🚀 Sending '{selected_video}' data to Webhook...")

try:
    # JSON format mein data bhej rahe hain (Webhook ke liye sabse best)
    response = requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    
    print("✅ Success! Data webhook par chala gaya.")
    print("📤 Payload Sent:\n", json.dumps(payload, indent=2))
    
    # 9. Success hone ke baad hi History file update karna
    with open(HISTORY_FILE, 'a') as f:
        f.write(selected_video + '\n')
    print(f"📝 History update ho gayi: '{selected_video}' saved to history.txt")

except requests.exceptions.RequestException as e:
    print(f"❌ Webhook fail ho gaya: {e}")
    exit(1)
