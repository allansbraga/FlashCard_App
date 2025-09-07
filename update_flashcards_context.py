import sqlite3
import os

def get_db_connection():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect('flashcards.db')

def update_flashcards_with_context():
    """Atualiza os flashcards existentes com contexto adequado"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Dicionário com as atualizações contextualizadas
    updates = {
        # Phrasal Verbs com contexto
        "Give up": "I give up because this task is too complicated",
        "Look forward to": "I look forward to meeting you next week",
        "Run out of": "We ran out of coffee this morning",
        "Put off": "Don't put off your homework until tomorrow",
        "Get along with": "She gets along with her coworkers very well",
        "Turn down": "He turned down the job offer yesterday",
        "Bring up": "Please don't bring up that topic again",
        "Come across": "I came across an interesting article today",
        "Figure out": "Can you figure out this math problem?",
        "Take after": "She takes after her mother in personality",
        "Break down": "My car broke down on the highway",
        "Call off": "They called off the meeting due to rain",
        "Carry on": "Please carry on with your presentation",
        "Check out": "Let's check out that new restaurant tonight",
        "Drop by": "Feel free to drop by my office anytime",
        
        # Present Perfect com contexto
        "I have lived": "I have lived in this city for five years",
        "She has worked": "She has worked at this company since 2020",
        "They have traveled": "They have traveled to many countries together",
        "We have studied": "We have studied English for three months",
        "He has finished": "He has finished his homework already",
        "You have seen": "You have seen this movie before, haven't you?",
        "I have never been": "I have never been to Japan, but I'd love to go",
        "She has already eaten": "She has already eaten lunch, so she's not hungry",
        "They have just arrived": "They have just arrived at the airport",
        "We have known": "We have known each other since childhood",
        
        # Past Perfect com contexto
        "I had finished": "I had finished my work before the meeting started",
        "They had arrived": "They had arrived at the party before we got there",
        "She had studied": "She had studied French before moving to Paris",
        "We had eaten": "We had eaten dinner before the movie began",
        "He had left": "He had left the office when I called him",
        "You had seen": "You had seen that documentary before we watched it together",
        "I had never visited": "I had never visited Europe until last summer",
        "They had already decided": "They had already decided to move before the announcement",
        
        # Travel Vocabulary com contexto
        "Airport": "The airport was very crowded during the holiday season",
        "Boarding pass": "Don't forget to print your boarding pass before the flight",
        "Departure gate": "The departure gate for flight 205 is B12",
        "Baggage claim": "Meet me at the baggage claim area after you land",
        "Customs": "We had to wait in line at customs for an hour",
        "Passport control": "Passport control was surprisingly quick today",
        "Hotel reservation": "I made a hotel reservation for three nights",
        "Room service": "We ordered room service because we were too tired to go out",
        "Tourist attraction": "The Eiffel Tower is the most famous tourist attraction in Paris",
        "Currency exchange": "I need to find a currency exchange office at the airport",
        "Travel insurance": "Travel insurance is essential for international trips",
        "Itinerary": "Our travel itinerary includes visits to five different cities",
        "Sightseeing": "We spent the whole day sightseeing in the old town",
        "Souvenir": "I bought a beautiful souvenir for my sister",
        
        # Business Vocabulary com contexto
        "Meeting": "The board meeting is scheduled for 2 PM today",
        "Deadline": "We need to meet the project deadline by Friday",
        "Budget": "The marketing budget for this quarter has been approved",
        "Profit": "The company's profit increased by 15% this year",
        "Revenue": "Our monthly revenue exceeded expectations",
        "Investment": "The new investment will help expand our operations",
        "Stakeholder": "All stakeholders must approve the new policy",
        "Quarterly report": "The quarterly report shows positive growth trends",
        "Market share": "Our market share has grown significantly this year",
        "Business plan": "The business plan needs to be revised before presentation",
        "Cash flow": "We need to improve our cash flow management",
        "ROI (Return on Investment)": "The ROI on this project is expected to be 25%",
        "Networking": "Networking events are great for building business relationships",
        "Presentation": "Her presentation impressed all the clients",
        "Negotiation": "The contract negotiation took longer than expected",
        "Partnership": "Our partnership with that company has been very successful",
        "Merger": "The merger between the two companies was announced yesterday",
        "Acquisition": "The acquisition will strengthen our market position",
        "Outsourcing": "Outsourcing IT services helped reduce operational costs",
        "Human Resources": "Human Resources is handling the recruitment process",
        
        # Travel Phrases com contexto
        "Where is the nearest ATM?": "Excuse me, where is the nearest ATM? I need to withdraw some cash",
        "How much does it cost?": "How much does it cost to take a taxi to the city center?",
        "Can you recommend a good restaurant?": "Can you recommend a good restaurant that serves local cuisine?",
        "I'd like to book a table for two": "I'd like to book a table for two at 7 PM tonight",
        "Excuse me, where is the bathroom?": "Excuse me, where is the bathroom? I really need to use it",
        "Could you help me with directions?": "Could you help me with directions to the train station?",
        "I'm looking for a taxi": "I'm looking for a taxi to take me to the airport",
        "What time does the museum open?": "What time does the museum open on Sundays?",
        "Is there Wi-Fi available?": "Is there Wi-Fi available in this hotel lobby?",
        "I need to exchange money": "I need to exchange money before I go shopping",
        
        # Business Phrases com contexto
        "Let's schedule a meeting": "Let's schedule a meeting to discuss the new project proposal",
        "I'll get back to you on that": "I'll get back to you on that after I check with my team",
        "Could you send me the proposal?": "Could you send me the proposal by email before tomorrow?",
        "We need to meet the deadline": "We need to meet the deadline or we'll lose the client",
        "Let's think outside the box": "Let's think outside the box to find a creative solution",
        "We're on the same page": "Great! It sounds like we're on the same page about this",
        "Let's touch base next week": "Let's touch base next week to see how the project is progressing",
        "I'll keep you in the loop": "I'll keep you in the loop about any important updates",
        "We need to cut costs": "We need to cut costs without compromising quality",
        "The project is on track": "The project is on track to be completed ahead of schedule"
    }
    
    print("🔄 Atualizando flashcards com contexto...")
    
    updated_count = 0
    for old_content, new_content in updates.items():
        cursor.execute('''
            UPDATE flashcards 
            SET front_content = ? 
            WHERE front_content = ?
        ''', (new_content, old_content))
        
        if cursor.rowcount > 0:
            print(f"✓ Atualizado: {old_content} → {new_content}")
            updated_count += cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Sucesso! {updated_count} flashcards atualizados com contexto!")
    print("\nTodos os flashcards agora incluem frases completas e contextualizadas para melhor aprendizado.")

if __name__ == "__main__":
    update_flashcards_with_context()