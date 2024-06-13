import os
import json
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Define Pydantic models for input validation
class LocationDetails(BaseModel):
    location: str
    mode: str
    filming_permits: bool

class UserInput(BaseModel):
    projectName: str
    contentType: str
    budget: float
    description: str
    additional_details: str
    locationDetails: List[LocationDetails]
    ai_suggestions: bool
    crew: Dict[str, int]

# Sample crew database (mock data for demonstration)
try:
    print(os.getcwd())
    with open('crewdata.json', 'r') as f:
        crew_database = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("crewdata.json file not found", os.getcwd())

def parse_user_input(user_input: UserInput):
    """Parse user input to extract relevant project details."""
    project_details = {
        "projectName": user_input['projectName'],
        "contentType": user_input['contentType'],
        "budget": user_input['budget'],
        "description": user_input['description'],
        "additional_details": user_input['additional_details'],
        "locationDetails": user_input['locationDetails'],
        "crew": user_input['crew']
    }
    return project_details

def filter_crew_by_role(crew_database, role):
    """Filter the crew database to find members matching the specified role."""
    return [crew for crew in crew_database if crew['roleJobTitle'] == role]

def select_best_crew_member(crew_list, project_details):
    """Select the best crew member based on project requirements and crew member details."""
    selected_crew = sorted(crew_list, key=lambda x: (x['yoe'], -x['minRatePerDay']))[0]
    return selected_crew

def generate_crew_output(selected_crew, role):
    """Generate the output format for the selected crew member."""
    output = {
        role: {
            "UserId": selected_crew["userid"],
            "Preferred_because": f"{selected_crew['name']} has extensive experience in {', '.join(selected_crew['expertise'])}. They are based in {selected_crew['location']} and their rate fits within the budget.",
            "user_details": selected_crew
        }
    }
    return output

def generate_output_for_all_roles(user_input: UserInput):
    """Generate the output for all required roles in the project."""
    project_details = parse_user_input(user_input)
    crew_output = []

    for role, count in project_details['crew'].items():
        crew_list = filter_crew_by_role(crew_database, role)
        if crew_list:
            selected_crew = select_best_crew_member(crew_list, project_details)
            crew_output.append(generate_crew_output(selected_crew, role))
    
    return crew_output

