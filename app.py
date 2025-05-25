from flask import Flask, request
import google.generativeai as genai
import os
from flask import send_from_directory

app = Flask(__name__)

@app.route('/<filename>')
def serve_root_files(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(root_dir, filename)


@app.route('/')
def home():
    return """
    <html>
        <head>
            <title style="color:purple;">CareerGuide</title>
            <style>
                body {
                    background-color: white;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
.container {
    background-color: powderblue;
    max-width: 1000px;
    margin: 40px auto;
    padding: 20px 40px;
    border-radius: 8px;
    box-sizing: border-box;
}
                h1 {
                    font-family: 'Times New Roman', serif;
                    font-size: 18px;
                    color: black;
                }
                label {
                    color: black;
                    font-weight: bold;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 8px;
                    margin: 8px 0 16px 0;
                    box-sizing: border-box;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                input[type="submit"] {
                    background-color: #4a90e2;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #357ABD;
                }
                p {
                    color: black;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to StreamGuide! 👋 Feeling unsure about your next steps?
                Our AI-powered career guidance will help you discover the best academic streams
                based on your interests and strengths. Start the quiz now and unlock your potential! 🚀 </h1>
                <form action="/recommend" method="get">
                    <label>1) Enter The subjects you find interesting (comma separated):</label><br>
                    <input type="text" name="interests1"><br>

                    <label>2) Enter the subjects you excel at (comma separated):</label><br>
                    <input type="text" name="interests2"><br>

                    <label>3) Enter the subjects struggle at (comma separated):</label><br>
                    <input type="text" name="struggle"><br>

                    <label>4) Which area of a subject do you find interesting (comma separated):</label><br>
                    <input type="text" name="sub_area"><br>

                    <label>5) Which industry are you interested in (comma separated):</label><br>
                    <input type="text" name="indust_area"><br>

                    <label>6) What are your hobbies (comma separated):</label><br>
                    <input type="text" name="hobbies"><br>

<label>7) What kind of problems do you find interesting:</label><br>
<input type="radio" name="problems" value="Solving real-world challenges"> Solving real-world challenges<br>
<input type="radio" name="problems" value="Designing creative solutions"> Designing creative solutions<br>
<input type="radio" name="problems" value="Analyzing data and patterns"> Analyzing data and patterns<br>
<input type="radio" name="problems" value="Building and improving systems"> Building and improving systems<br>

                    <label>8) What are you naturally good at?</label><br>
                    <input type="text" name="natural_skill"><br>

                    <label>9) Are you more interested in individual projects or group projects?</label><br>
                    <input type="text" name="Teamwork"><br>

                    <label>10) What are your weaknessses and strenghts? How might they your career choice?</label><br>
                    <input type="text" name="strengths_weaknesses"><br>

<label>11) What kind of learning do you prefer?</label><br>
<input type="radio" name="learning_style" value="Learning through real world projects"> Learning through real world projects<br>
<input type="radio" name="learning_style" value="Visual learning"> Visual learning<br>
<input type="radio" name="learning_style" value="Mentor-guided learning"> Mentor-guided learning<br>
<input type="radio" name="learning_style" value="Self-paced learning"> Self-paced learning<br>

                    <label>12) What matters most to you in a career?(e.g. money, stabilities, creativity, status.)</label><br>
                    <input type="text" name="Matters"><br>

<label>13) Are you comfortable shifting locations within India for studies?</label><br>           
<input type="radio" name="location_shift" value="Yes"> Yes<br>
<input type="radio" name="location_shift" value="No"> no<br>
<input type="radio" name="location_shift" value="Not sure"> Not sure<br>

                    <label>14) What type of college education do you think your family can comfortably support financially</label><br>
                    <input type="text" name="financial"><br> 
                     
                    <input type="submit" value="Get Recommendations">
                </form>
                <p>Note: Enter multiple values separated by commas.</p>
            </div>
        </body>
    </html>
    """

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit()
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY) 
        model = genai.GenerativeModel('gemini-2.0-flash') 
        print("Gemini AI Model configured successfully.")
    except Exception as e:
        print(f"Error configuring Gemini AI: {e}")
        exit()

@app.route('/recommend', methods=['GET'])
def recommend_stream():
    print("Received request to recommend stream")
    
    # Parse comma separated values into lists
    def parse_list(param):
        val = request.args.get(param, '')
        return [x.strip() for x in val.split(',')] if val else []

    user_interests1 = parse_list('interests1')
    user_interests2 = parse_list('interests2')
    user_struggle = parse_list('struggle')
    user_sub_area = parse_list('sub_area')
    user_indust_area = parse_list('indust_area')
    user_hobbies = parse_list('hobbies')
    user_problems = request.args.get('problems', '')
    user_natural_skill = parse_list('natural_skill')
    user_teamwork = request.args.get('Teamwork', '')
    user_strengths_weaknesses = request.args.get('strengths_weaknesses', '')
    user_learning_style = request.args.get('learning_style', '')
    user_location_shift = request.args.get('location_shift', '')
    user_matters = parse_list('Matters')
    user_financial = request.args.get('financial', '')

    prompt = f'''I am a high school student exploring high school course options and i am in india. I study in CBSE board.
My interests include: {', '.join(user_interests1) if user_interests1 else 'None specified'}.
Subjects I excel at: {', '.join(user_interests2) if user_interests2 else 'None specified'}.
Subjects I struggle with: {', '.join(user_struggle) if user_struggle else 'None specified'}.
Specific subject areas I find interesting: {', '.join(user_sub_area) if user_sub_area else 'None specified'}.
Industry areas that interest me: {', '.join(user_indust_area) if user_indust_area else 'None specified'}.
My hobbies are: {', '.join(user_hobbies) if user_hobbies else 'None specified'}.
I enjoy solving problems involving: {user_problems if user_problems else 'Not specified'}.
My natural skills include: {', '.join(user_natural_skill) if user_natural_skill else 'None specified'}.
I prefer working on: {user_teamwork if user_teamwork else 'Not specified'}.
My strengths and weaknesses are: {user_strengths_weaknesses if user_strengths_weaknesses else 'Not specified'}.
I like learning through: {user_learning_style if user_learning_style else 'Not specified'}.
I am comfortable shifting locations within India for studies: {user_location_shift if user_location_shift else 'Not specified'}.
My family's financial support for college education: {user_financial if user_financial else 'Not specified'}.
what matters most to me in a career is: {', '.join(user_matters) if user_matters else 'Not specified'}.

Based *only* on this information, suggest 2-3 specific academic streams or subject combinations suitable for me after high school. For each suggestion, briefly explain why it fits my profile. Focus on standard academic paths like Science (Physics, Chemistry, Math/Biology), Commerce, Arts/Humanities, and potential specializations within them. If my interests are not the standard ones, suggest alternative streams or combinations.

Then, provide an extremely short and breif list of study resources. Provide resources related to the most recommended stream. Separate the recommendations and study resources sections with the delimiter "###".
'''

    prompt = f'''I am a high school student exploring high school course options and i am in india. I study in CBSE board.
My interests include: {', '.join(user_interests1) if user_interests1 else 'None specified'}.
Subjects I excel at: {', '.join(user_interests2) if user_interests2 else 'None specified'}.
Subjects I struggle with: {', '.join(user_struggle) if user_struggle else 'None specified'}.
Specific subject areas I find interesting: {', '.join(user_sub_area) if user_sub_area else 'None specified'}.
Industry areas that interest me: {', '.join(user_indust_area) if user_indust_area else 'None specified'}.
My hobbies are: {', '.join(user_hobbies) if user_hobbies else 'None specified'}.
I enjoy solving problems involving: {user_problems if user_problems else 'Not specified'}.
My natural skills include: {', '.join(user_natural_skill) if user_natural_skill else 'None specified'}.
I prefer working on: {user_teamwork if user_teamwork else 'Not specified'}.
My strengths and weaknesses are: {user_strengths_weaknesses if user_strengths_weaknesses else 'Not specified'}.
I like learning through: {user_learning_style if user_learning_style else 'Not specified'}.
what matters most to me in a career is: {', '.join(user_matters) if user_matters else 'Not specified'}.


Based *only* on this information, suggest 2-3 specific academic streams or subject combinations suitable for me after high school. For each suggestion, briefly explain why it fits my profile. Focus on standard academic paths like Science (Physics, Chemistry, Math/Biology), Commerce, Arts/Humanities, and potential specializations within them. If my interests are not the standard ones, suggest alternative streams or combinations.

Then, provide an extremely short and breif list of study resources. Provide resources related to the most recommended stream. Separate the recommendations and study resources sections with the delimiter "###".
'''

    try:
        response = model.generate_content(prompt)

        if hasattr(response, 'text'):
            full_response = response.text
            print(f"Gemini response received: {full_response}") 
            # Split the response by delimiter "###"
            parts = full_response.split("###")
            recommendations = parts[0].strip() if len(parts) > 0 else ""
            study_resources = parts[1].strip() if len(parts) > 1 else ""
            # Return styled HTML page with recommendations and study resources
            return f"""
            <html>
                <head>
                    <title>CareerGuide Recommendations</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            margin: 0;
                            padding: 0;
                            color: #333;
                            overflow-y: visible;
                        }}
                        .page-wrapper {{
                            display: flex;
                            min-height: 100vh;
                            align-items: flex-start;
                            padding-top: 0;
                            margin-top: 0;
                            gap: 0;
                            height: 100vh;
                        }}
                        .side-container {{
                            width: 200px;
                            background-color: #001f4d; /* dark blue */
                            color: white;
                            padding: 20px;  
                            box-sizing: border-box;
                            display: flex;
                            flex-direction: column;
                        }}
                        .left-container {{
                            border-right: 2px solid #003366;
                            white-space: pre-wrap;
                            font-size: 14px;
                        }}
                        .right-container {{
                            border-left: 2px solid #003366;
                        }}
                        .main-container {{
                            flex-grow: 1;
                            background: #fff;
                            padding: 20px;
                            box-sizing: border-box;
                            max-width: 800px;
                            margin: auto;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        }}
                        h1 {{
                            color: #4a90e2;
                            margin-top: 0;
                        }}
                        h2 {{
                            margin-top: 0;
                            margin-bottom: 10px;
                        }}
                        pre {{
                            white-space: pre-wrap;
                            font-size: 16px;
                            line-height: 1.5;
                        }}
                        a {{
                            display: inline-block;
                            margin-top: 20px;
                            text-decoration: none;
                            color: #4a90e2;
                            font-weight: bold;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                        .review {{
                            margin-bottom: 15px;
                        }}
                        .profile-name {{
                            font-weight: bold;
                            margin-bottom: 5px;
                        }}
                        .small-text {{
                            font-size: 0.9em;
                            color: #ccc;
                        }}
                    </style>
                </head>
                <body>
                    <div class="page-wrapper">
                        <div class="side-container left-container">
                            <h2>Study Resources</h2>
                            <pre>{study_resources}</pre>
                        </div>
                        <div class="main-container">
                            <h1>Your Career Recommendations</h1>
                            <pre>{recommendations}</pre>
                            <a href="/">&#8592; Back to Home</a>
                        </div>
                        <div class="side-container right-container">
                            <h2>Ratings and Reviews</h2>
                            <div class="review">
                                <div class="profile-name">Hannah</div>
                                <div>Excellent app. ⭐⭐⭐⭐⭐</div>
                            </div>
                            <div class="review">
                                <div class="profile-name">aarna</div>
                                <div>Excellent app. ⭐⭐⭐⭐✰</div>
                            </div>
                            <div class="review">

                                <div class="profile-name">Fatima Siddiqui</div>
                                <div>Provides accurate suggestions but UI is plain ⭐⭐⭐✰✰ </div>
                            </div>
                            <div class="review">
                                <div class="profile-name">Sarah Khan</div>
                                <div>It is fine but they should add more features. ⭐⭐⭐✰✰ </div>
                            </div>
                            <div class="review">
                                <div class="profile-name">Arif Khan</div>
                                <div>It is brilliant! ⭐⭐⭐⭐⭐</div>
                            </div>
                            <div class="small-text">See more reviews-></div>
                        </div>
                    </div>
                </body>
            </html>
            """
      
        elif hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
             error_message = f"Content blocked due to: {response.prompt_feedback.block_reason.name}"
             print(error_message)
             return f"""
             <html>
                <body>
                    <h2>Error</h2>
                    <p>{error_message}</p>
                    <a href="/">&#8592; Back to Home</a>
                </body>
             </html>
             """, 400
        else:
            print("Gemini response was empty or in an unexpected format.")
            return f"""
            <html>
                <body>
                    <h2>Error</h2>
                    <p>Failed to get recommendation from AI. The response was empty.</p>
                    <a href="/">&#8592; Back to Home</a>
                </body>
            </html>
            """, 500

    except Exception as e:
        print(f"Error during Gemini API call: {str(e)}")
        return f"""
        <html>
            <body>
                <h2>Error</h2>
                <p>An internal error occurred while generating recommendations.</p>
                <a href="/">&#8592; Back to Home</a>
            </body>
        </html>
        """, 500

if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set. Exiting.")
    elif 'model' not in globals():
        print("Gemini model initialization failed. Exiting.")
    else:
        print("Starting Flask server on http://127.0.0.1:5000")
        app.run(debug=True)
