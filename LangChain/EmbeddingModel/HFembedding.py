from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

embed = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

cricket_dataset = [
    # Core Mechanics & Field Setup
    "The cricket pitch is a central 22-yard long rectangular strip of clay or grass where the bowler delivers the ball to the active batsman, bounded by the popping crease.",
    "A standard cricket field is a large grass oval with no fixed dimensions, bounded by a rope known as the boundary, with three wooden stakes called wickets placed at each end of the pitch.",
    "An over in cricket consists of exactly six legal deliveries bowled consecutively by a single bowler from one end of the pitch, after which a new bowler takes over from the opposite end.",
    
    # Scoring Mechanics
    "Batsmen score runs by hitting the ball and physically running back and forth between the wickets, with each successful crossing counting as one run.",
    "A boundary four is awarded when a batsman hits the ball and it touches the ground before rolling past or bouncing over the boundary rope.",
    "A boundary six, the ultimate scoring shot, is awarded when the batsman hits the ball cleanly over the boundary rope through the air without it touching the playing field.",
    "Extra runs or penalties are awarded against the bowler as a Wide if the ball is delivered out of the batsman's reach, or a No-Ball for an illegal foot overstep or a dangerous high delivery.",
    "A Free Hit is awarded in limited-overs formats following a foot-fault No-Ball, meaning the batsman cannot be dismissed by most methods on the subsequent delivery.",
    
    # Methods of Dismissal
    "A batsman is dismissed as Bowled when the bowler's delivery misses the bat and directly strikes the wicket, knocking the bails off the top of the stumps.",
    "A Caught dismissal occurs when the batsman hits the ball into the air with their bat or a gloved hand, and a fielder catches it cleanly before it touches the ground.",
    "Leg Before Wicket or LBW is a dismissal where the ball strikes the batsman's leg pad instead of the bat, and the umpire judges that the ball would have gone on to hit the stumps.",
    "A Run Out occurs when the fielding team throws the ball and breaks the wicket while the batsmen are running, before the active batsman can ground their bat safely behind the crease.",
    "Stumped is a dismissal where the batsman steps past the safe crease line while attempting a shot, misses the ball, and the wicketkeeper immediately breaks the wicket with the ball.",
    
    # Formats of the Game
    "Test Cricket is the traditional five-day format of the game, featuring unlimited overs, red leather balls, white clothing, and requiring immense patience and psychological endurance.",
    "One Day Internationals or ODIs are limited-overs matches completed in a single day, capped at 50 overs per side, played with white balls and colored kits under floodlights.",
    "Twenty20 or T20 cricket is a fast-paced three-hour format limited to 20 overs per team, designed for maximum entertainment, explosive power-hitting, and high-risk strategies.",
    "The Indian Premier League or IPL is a massive global franchise T20 tournament that popularized advanced data analytics, strategic timeouts, and multi-million dollar player auctions.",
    
    # Legends and Historical Milestones
    "Sir Donald Bradman of Australia is widely regarded as the greatest batsman in history, retiring with an unmatched and historically anomalous Test batting average of 99.94.",
    "Sachin Tendulkar of India, known as the Little Master, holds the record for the most total runs in international cricket and is the only player to score 100 international centuries.",
    "Muttiah Muralitharan of Sri Lanka is the most successful spin bowler in cricket history, holding the record for the highest number of wickets in both Test matches with 800 and ODIs with 534.",
    "India's historic underdog victory against the dominant West Indies in the 1983 World Cup final at Lord's shifted the financial and cultural epicenter of global cricket to the subcontinent.",
    
    # Bowling Varieties & Tactics
    "Fast bowlers rely on sheer pace, swing, and seam movement to deceive the batsman, often targeting the pitch to generate sharp bounce or aiming at the toes with yorkers.",
    "Spin bowlers use their fingers or wrist to impart heavy revolutions on the ball, causing it to sharply change direction or turn upon bouncing off the pitch surface.",
    "The DRS or Decision Review System allows teams to challenge on-field umpire decisions using technologies like Hawk-Eye ball tracking, UltraEdge audio sensors, and Hot Spot infrared imaging."
]


dataset_embedding= embed.embed_documents(cricket_dataset)
query = "what is test cricket"
query_embedding = embed.embed_query(query)

scores = cosine_similarity([query_embedding],dataset_embedding)[0]
index = sorted(list(enumerate(scores)),key = lambda x: x[1])[-1][0]
print("Scores\n",scores)
print("index\n",index)
result = cricket_dataset[index]

print(result)