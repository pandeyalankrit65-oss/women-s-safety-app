from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Google Gemini API
genai.configure(api_key="AIzaSyCRH8PUTFIQ7FRkYxWRbvojcQe3y42xD-4")

@app.route('/')
def home():
    return render_template('index.html')  # Main page with Start Chat button

@app.route('/chat')
def chat():
    return render_template('chat.html')  # Chatbot UI

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    # Fine-tuned prompt to make responses better
    prompt = f"""
You are B-Break, an AI-powered chatbot designed to support individuals facing gender discrimination and domestic violence.  
Your goal is to provide **quick, action-oriented** help, ensuring users feel safe, heard, and empowered.  

🔹 **Tone:** Warm, understanding, and solution-driven.  
🔹 **Response Style:** Short (1-2 lines max), direct, and helpful.  
🔹 **What to Provide:** Emotional support, emergency contacts, legal guidance, and self-care strategies.  
🔹 **No Generic Replies:** Instead of just listening, always **offer actionable solutions.**  

🚨 **How to Respond Based on the User's Needs:**  
1️⃣ **If the user is feeling anxious or overwhelmed:**  
   - Provide **self-care tips** (breathing exercises, grounding techniques).  
   - Offer **motivational support** (affirmations, success stories).  

2️⃣ **If the user feels unsafe (but not in immediate danger):**  
   - Suggest **safety planning steps** (packing essentials, securing documents).  
   - Share **legal rights information** (restraining orders, workplace protections).  
   - Connect them to **NGOs & helplines** in their area.  

3️⃣ **If the user is in IMMEDIATE danger (SOS mode):**  
   - Give **crisis helpline numbers** based on location.  
   - Suggest **safe exit strategies** to leave an unsafe environment.  
   - (Optional) Guide them on how to contact **a trusted person** discreetly.  

4️⃣ **If the user needs career, financial, or long-term help:**  
   - Offer resources for **job support, financial aid, and therapy options.**  
   - Provide links to **empowerment tools & survivor forums.**  

User: {user_input}  
B-Break:  

    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return jsonify({"response": response.text.strip()})  # Clean response

    except Exception as e:
        return jsonify({"response": "Oops! Something went wrong. Try again later."})

if __name__ == '__main__':
    app.run(debug=True)