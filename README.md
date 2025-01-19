# HacknRoll2025
The product built for Hack&amp;Roll 2025.

💘 Cupid Arrow - Love at Your Fingertips! 💘
Looking for a spark? Cupid Arrow on Telegram brings love and connection closer than ever. With instant matching, private chats, and a fun, user-friendly experience, finding your special someone has never been easier. Join the Cupid community today and let love strike where you least expect it! 💬❤️

### Inspiration
Looking for a spark? Cupid Arrow is the ultimate Telegram bot designed to bring love and connection closer than ever. With its smart matching algorithm, Cupid Arrow scours its database to find the best match for you. Enjoy private, seamless chats and a fun, user-friendly experience that makes meeting someone special effortless.💘 

Just a few taps away: share your preferences, let the bot work its magic, and connect with like-minded individuals instantly.

Join the Cupid community today, where Cupid Arrow helps you find the perfect match in no time. Let love strike where you least expect it! 💬❤️
   
### What it does
Cupid Arrow Telegram bot facilitates seamless matchmaking by performing the following actions:

User Initialization: When the user initiates the bot with /start, the bot welcomes them and creates a user profile in its database.

Matching Requests: Users can request matches based on their preferences. If the user hasn't taken the quiz or if the quiz is outdated, the bot redirects them to take the quiz (UC3). Otherwise, it runs its matching algorithm to identify and return the top 3-10 most compatible matches.

User Quiz: The bot gathers detailed user preferences by prompting a series of quiz questions. User responses update their profile in real-time to enhance matchmaking accuracy.

Account Removal: Users can request to delete their account, and the bot ensures all associated data is removed from its database.

In summary, Cupid Arrow efficiently connects users by maintaining updated profiles, matching them with the best-suited individuals, and providing full control over their data.
  
### How we built it

**Telegram Interaction**: Managed using `python-telegram-bot` API for smooth communication between the bot and users.
   
**Database**: User data is stored in a `sqlite` database for lightweight and efficient management.
  
**Data Processing**: numpy and scikit-learn are used to preprocess user data and enable effective matching.
  
**Dimensionality Reduction**: Principal Component Analysis (PCA) is applied to reduce the dimensionality of user data to two dimensions, simplifying and optimizing the matching process.  

**Matching Algorithm Overview**:
Setup: Start with the user's feature vector v (an m-dimensional vector) and a set of feature vectors S. The goal is to find a subset S' ⊆ S of size k such that no vectors in S are closer to v than the vectors in S′.
Dimensionality Reduction: Apply PCA to project v and S into 3D space, improving computational efficiency.
Quick Selection: Use the quick select algorithm to find the k-th closest vector efficiently.

### Accomplishments that we're proud of

### Challenges we ran into
1. Explore on the correct algorithm for matching
2. Learn telegram API

### What we learned

### Built With
anyio==4.8.0
certifi==2024.12.14
greenlet==3.1.1
h11==0.14.0
httpcore==1.0.7
httpx==0.28.1
idna==3.10
joblib==1.4.2
numpy==2.2.1
python-dotenv==1.0.1
python-telegram-bot==21.10
scikit-learn==1.6.1
scipy==1.15.1
sniffio==1.3.1
SQLAlchemy==2.0.37
threadpoolctl==3.5.0
typing_extensions==4.12.2

### Try it out
