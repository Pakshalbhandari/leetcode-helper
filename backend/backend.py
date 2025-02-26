from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.5, 
            groq_api_key=os.getenv("GROQ_API_KEY"), 
            model_name="llama-3.3-70b-versatile", 
            max_retries=2
        )

    def generate_solution_outline(self, problem_description):
        prompt_template = PromptTemplate.from_template(
            """
            ### PROBLEM DESCRIPTION:
            {problem_description}
            ### INSTRUCTION:
            Provide a solution outline for the given problem description. The outline should include problem understanding, approach, edge cases, and time/space complexity analysis and code in python with comments. 
            ### SOLUTION OUTLINE (NO PREAMBLE):
            """
        )
        chain = prompt_template | self.llm
        response = chain.invoke(input={"problem_description": problem_description})
        
        # Directly return the raw content (as markdown or text)
        res_content = response.content  
        return res_content

chain = Chain()

# Handle OPTIONS request explicitly
@app.route('/generate_solution', methods=['POST', 'OPTIONS'])
def generate_solution():
    # Allow the OPTIONS preflight request to pass through
    if request.method == 'OPTIONS':
        print("HEREEE")
        return jsonify({'message': 'CORS preflight response'}), 200

    try:
        data = request.get_json()
        print(f"Raw data: {request.data}")  # Log the raw request data

        problem_description = data.get("problem_description", "")
        if not problem_description:
            return jsonify({"error": "Problem description is required"}), 400
        solution_outline = chain.generate_solution_outline(problem_description)
        print("Bye")
        return jsonify({"solutionOutline": solution_outline})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if os.getenv("GROQ_API_KEY") is None:
        raise Exception("Please set the environment variable GROQ_API_KEY")
    app.run(debug=True)
