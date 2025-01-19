# HacknRoll2025
The product built for Hack&amp;Roll 2025.

💘 Cupid Arrow - Love at Your Fingertips! 💘
Looking for a spark? Cupid Arrow on Telegram brings love and connection closer than ever. With instant matching, private chats, and a fun, user-friendly experience, finding your special someone has never been easier. Join the Cupid community today and let love strike where you least expect it! 💬❤️

### Inspiration
Looking for a spark? Cupid Arrow is the ultimate Telegram bot designed to bring love and connection closer than ever. With its smart matching algorithm, Cupid Arrow scours its database to find the top 3 best matches for you. Enjoy private, seamless chats and a fun, user-friendly experience that makes meeting someone special effortless.💘 

Just a few taps away: share your preferences, let the bot work its magic, and connect with like-minded individuals instantly.

Join the Cupid community today, where Cupid Arrow helps you find the perfect match in no time. Let love strike where you least expect it! 💬❤️
   
### What it does
Cupid Arrow Telegram bot facilitates seamless matchmaking by performing the following actions:

User Initialization: When the user initiates the bot with /start, the bot welcomes them and creates a user profile in its database.

Matching Requests: Users can request matches based on their preferences. Before taking the quiz, the user can input hhis gender and age. If the user hasn't taken the quiz or if the quiz is outdated, the bot redirects them to take the quiz. Otherwise, it runs its matching algorithm to identify and return the top 3 most compatible matches.

User Quiz: The bot gathers detailed user preferences by prompting a series of 8 quiz questions. User responses update their profile in real-time to enhance matchmaking accuracy.

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
Advanced Matching Algorithm:   
Successfully implemented a robust matchmaking algorithm that utilizes PCA for dimensionality reduction and quick select for efficient and accurate user matching.
  
Streamlined User Experience:  
Designed an intuitive, user-friendly interface using the python-telegram-bot API, ensuring seamless interactions between users and the bot.  
  
Efficient Data Handling:  
Integrated a lightweight SQLite database for efficient storage and management of user data, allowing fast retrieval and processing during matches.  
  
Data-Driven Insights:  
Leveraged cutting-edge tools like numpy and scikit-learn to preprocess user data and ensure high accuracy in match recommendations.  
  
Scalability and Optimization:  
Utilized Principal Component Analysis (PCA) to optimize the computational performance of the matchmaking algorithm, reducing complexity and improving scalability.
  
Comprehensive Privacy Controls:   
Empowered users with control over their data by implementing an account deletion feature that ensures secure removal of user information from the database.
  
### Challenges we ran into
Exploring the Correct Algorithm for Matching:   
Finding an efficient and accurate matching algorithm was a key challenge. While k-d trees were considered, their computational expense for constructing new trees led us to utilize the quick select algorithm.
   
Learning Telegram API:  
Understanding the python-telegram-bot API to handle user interactions, bot commands, and error scenarios was a learning curve. Integrating the bot's logic with real-time user inputs demanded a thorough understanding of the API's capabilities and limitations.  
   
Sorting with Quick Select:  
Adapting the quick select algorithm for sorting user data based on proximity in reduced dimensions was challenging. Implementing it efficiently while maintaining accuracy and managing edge cases required meticulous attention to algorithm design and debugging.  
  
Dimensionality Reduction with PCA:  
Applying PCA to reduce the dimensions of user data was another hurdle. Ensuring that the reduced dimensions retained enough meaningful information for accurate matches involved careful tuning and validation.  
  
Data Management and Privacy:  
Ensuring efficient data handling, from storing user profiles in SQLite to managing real-time updates, was critical. Additionally, implementing a robust account deletion mechanism to address privacy concerns required precision and care.  

### What we learned

Firstly, we gained valuable experience in building a Telegram bot using the Python-Telegram-Bot API for the first time. We explored the entire process of learning the new API and developed an understanding of how to create a seamless and intuitive Telegram user experience from scratch.

Secondly, we had the opportunity to deepen our knowledge of relevant algorithms, such as QuickSelect. Additionally, we thoroughly examined the application of a combination of Principal Component Analysis (PCA) and Euclidean distance. This helped us become familiar with effective matching algorithms, particularly for scenarios involving high-dimensional metric spaces.

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
@CAGolddirio123_bot
