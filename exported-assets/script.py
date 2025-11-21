# Complete SEN Question-Answer Generator for Microsoft Forms Survey
import json
import csv
import random
import requests
from datetime import datetime
import pandas as pd


class SENQuestionGenerator:
    def __init__(self, openai_api_key=None):
        self.openai_api_key = openai_api_key

        # SEN Categories from UK Education System
        self.sen_categories = {
            "ASD": "Autism Spectrum Disorder",
            "ADHD": "Attention Deficit Hyperactivity Disorder",
            "SEMH": "Social, Emotional, Mental Health",
            "SLCN": "Speech, Language, Communication Needs",
            "MLD": "Moderate Learning Difficulties",
            "SPLD": "Specific Learning Difficulties",
            "PD": "Physical Disability",
            "VI": "Visual Impairment",
            "HI": "Hearing Impairment"
        }

        # Age groups and subjects
        self.age_groups = ["Early Years (3-5)", "Key Stage 1 (5-7)",
                           "Key Stage 2 (7-11)", "Key Stage 3 (11-14)", "Key Stage 4 (14-16)"]
        self.subjects = ["Mathematics", "English", "Science",
                         "Art", "PE", "Social Skills", "Life Skills"]

        # Common SEN challenges and scenarios
        self.challenge_templates = [
            "A student with {sen_type} in {age_group} is struggling with {subject}. They {specific_challenge}. What intervention strategies would you recommend?",
            "During {activity}, a {age_group} student with {sen_type} {behavior_issue}. How would you adapt your teaching approach?",
            "A {sen_type} student finds it difficult to {skill_area} in {subject} lessons. What accommodations would be most effective?",
            "In your {age_group} class, a student with {sen_type} {social_challenge}. What support strategies would you implement?",
            "A student with {sen_type} {learning_difficulty} when working on {subject} tasks. How would you modify the activity?"
        ]

        # Specific challenges by SEN type
        self.specific_challenges = {
            "ASD": [
                "becomes overwhelmed by sensory input",
                "struggles with social interactions during group work",
                "has difficulty with transitions between activities",
                "shows repetitive behaviors that distract others",
                "finds abstract concepts challenging to understand"
            ],
            "ADHD": [
                "cannot sit still for extended periods",
                "gets easily distracted by environmental stimuli",
                "struggles to follow multi-step instructions",
                "has difficulty organizing their work materials",
                "shows impulsive behavior during lessons"
            ],
            "SEMH": [
                "displays anxiety about participating in class",
                "shows anger outbursts when frustrated",
                "avoids challenging tasks due to fear of failure",
                "has difficulty regulating emotions during conflicts",
                "struggles with self-esteem and confidence"
            ],
            "SLCN": [
                "has difficulty expressing their thoughts clearly",
                "struggles to understand complex verbal instructions",
                "finds it hard to participate in discussions",
                "has trouble with reading comprehension",
                "shows frustration when not understood by peers"
            ]
        }

    def generate_llm_responses(self, scenario, num_responses=4):
        """
        Generate multiple LLM responses for each scenario
        Since we don't have actual OpenAI API, we'll create realistic sample responses
        """
        responses = []

        # Sample response templates for different types of interventions
        response_templates = [
            {
                "type": "Environmental",
                "response": "Create a calm, structured environment with visual supports and clear routines. Use noise-cancelling headphones if needed and provide a designated quiet space for breaks."
            },
            {
                "type": "Instructional",
                "response": "Break tasks into smaller, manageable steps with visual cues. Use multi-sensory teaching approaches and provide frequent positive reinforcement."
            },
            {
                "type": "Social",
                "response": "Implement peer buddy systems and social stories. Practice social skills explicitly and provide opportunities for structured social interaction."
            },
            {
                "type": "Behavioral",
                "response": "Use positive behavior support strategies with clear expectations. Implement a token economy system and teach self-regulation techniques."
            },
            {
                "type": "Assessment",
                "response": "Modify assessment methods using alternative formats. Allow extra time and provide assistive technology where appropriate."
            }
        ]

        # Select appropriate responses based on scenario content
        selected_responses = random.sample(
            response_templates, min(num_responses, len(response_templates)))

        for i, template in enumerate(selected_responses):
            response = {
                "id": f"response_{i+1}",
                "type": template["type"],
                "content": template["response"],
                # Simulated quality score
                "quality_score": random.uniform(0.6, 0.95)
            }
            responses.append(response)

        return responses

    def create_scenario(self, sen_type, age_group, subject):
        """Create a realistic SEN scenario"""
        template = random.choice(self.challenge_templates)
        specific_challenge = random.choice(self.specific_challenges.get(
            sen_type, ["faces learning difficulties"]))

        scenario = template.format(
            sen_type=self.sen_categories[sen_type],
            age_group=age_group,
            subject=subject,
            specific_challenge=specific_challenge,
            activity=f"{subject} lesson",
            behavior_issue=specific_challenge,
            skill_area=f"concentrate on {subject.lower()} tasks",
            social_challenge=specific_challenge,
            learning_difficulty=specific_challenge
        )

        return {
            "id": f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}",
            "sen_category": sen_type,
            "sen_full_name": self.sen_categories[sen_type],
            "age_group": age_group,
            "subject": subject,
            "scenario_text": scenario,
            "difficulty_level": random.choice(["Low", "Medium", "High"]),
            "priority": random.choice(["High", "Medium", "Low"])
        }

    def generate_question_set(self, num_questions=20):
        """Generate a set of SEN scenarios with multiple LLM responses"""
        questions = []

        for i in range(num_questions):
            # Randomly select parameters
            sen_type = random.choice(list(self.sen_categories.keys()))
            age_group = random.choice(self.age_groups)
            subject = random.choice(self.subjects)

            # Create scenario
            scenario = self.create_scenario(sen_type, age_group, subject)

            # Generate multiple LLM responses
            llm_responses = self.generate_llm_responses(
                scenario["scenario_text"])

            question_data = {
                **scenario,
                "llm_responses": llm_responses,
                "created_date": datetime.now().isoformat()
            }

            questions.append(question_data)

        return questions

    def format_for_microsoft_forms(self, questions):
        """Format questions for easy copy-paste into Microsoft Forms"""
        forms_data = []

        for i, question in enumerate(questions, 1):
            # Format the main question
            question_text = f"Question {i}: {question['scenario_text']}\n\n"
            question_text += f"SEN Category: {question['sen_full_name']}\n"
            question_text += f"Age Group: {question['age_group']}\n"
            question_text += f"Subject: {question['subject']}\n\n"
            question_text += "Please select the BEST response from the options below, or choose 'Other' to provide your own improved answer:"

            # Format response options
            options = []
            for j, response in enumerate(question['llm_responses'], 1):
                option_text = f"Option {j} ({response['type']}): {response['content']}"
                options.append(option_text)

            # Add "Other" option for teacher improvements
            options.append(
                "Other (Please specify your improved response in the text box below)")

            forms_question = {
                "question_number": i,
                "question_text": question_text,
                "question_type": "Multiple Choice",
                "options": options,
                "required": True,
                "follow_up_text": "If you selected 'Other', please provide your improved response:",
                "metadata": {
                    "sen_category": question['sen_category'],
                    "age_group": question['age_group'],
                    "subject": question['subject'],
                    "scenario_id": question['id']
                }
            }

            forms_data.append(forms_question)

        return forms_data

    def export_to_csv(self, questions, filename="sen_survey_questions.csv"):
        """Export questions to CSV for easy import/reference"""
        rows = []

        for question in questions:
            base_row = {
                "Question_ID": question['id'],
                "SEN_Category": question['sen_category'],
                "Age_Group": question['age_group'],
                "Subject": question['subject'],
                "Scenario": question['scenario_text'],
                "Created_Date": question['created_date']
            }

            # Add each LLM response as separate columns
            for i, response in enumerate(question['llm_responses'], 1):
                base_row[f"LLM_Response_{i}_Type"] = response['type']
                base_row[f"LLM_Response_{i}_Content"] = response['content']
                base_row[f"LLM_Response_{i}_Quality"] = response['quality_score']

            rows.append(base_row)

        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        print(f"Questions exported to {filename}")
        return filename

    def create_forms_import_file(self, forms_data, filename="microsoft_forms_import.txt"):
        """Create a text file with formatted questions for Microsoft Forms"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("MICROSOFT FORMS SURVEY QUESTIONS - SEN Teacher Feedback\n")
            f.write("="*60 + "\n\n")
            f.write("Instructions for Microsoft Forms Setup:\n")
            f.write("1. Create a new Microsoft Form\n")
            f.write(
                "2. For each question below, create a 'Multiple Choice' question\n")
            f.write("3. Copy the question text and all options\n")
            f.write("4. Enable 'Other' option for teacher improvements\n")
            f.write(
                "5. Add a text box after each multiple choice for detailed feedback\n\n")
            f.write("="*60 + "\n\n")

            for question_data in forms_data:
                f.write(f"QUESTION {question_data['question_number']}:\n")
                f.write("-" * 40 + "\n")
                f.write(f"{question_data['question_text']}\n\n")

                f.write("OPTIONS:\n")
                for i, option in enumerate(question_data['options'], 1):
                    f.write(f"{i}. {option}\n")

                f.write(
                    f"\nFOLLOW-UP TEXT BOX: {question_data['follow_up_text']}\n")
                f.write("\n" + "="*60 + "\n\n")

        print(f"Microsoft Forms import file created: {filename}")
        return filename


# Initialize the generator
generator = SENQuestionGenerator()

# Generate question set
print("Generating SEN questions and answers...")
questions = generator.generate_question_set(
    num_questions=10)  # Start with 10 for testing

print(f"Generated {len(questions)} questions successfully!")

# Show first question as example
if questions:
    print("\nExample Question:")
    print("-" * 50)
    print(f"Scenario: {questions[0]['scenario_text']}")
    print(f"SEN Category: {questions[0]['sen_full_name']}")
    print(f"Age Group: {questions[0]['age_group']}")
    print(f"Subject: {questions[0]['subject']}")
    print("\nLLM Response Options:")
    for i, response in enumerate(questions[0]['llm_responses'], 1):
        print(f"{i}. ({response['type']}) {response['content']}")
