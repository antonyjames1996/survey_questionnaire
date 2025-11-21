# Complete SEN Teacher Query and LLM Answer Generator for Microsoft Forms Survey
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

        # **UPDATED: Teacher Question Templates**
        self.teacher_question_templates = [
            # Strategy/Intervention
            "A teacher has a {age_group} student with {sen_type} struggling with {subject}. What are the **three most effective, quick-to-implement** intervention strategies for this specific {focus_point}?",
            # Resource/Differentiation
            "What specific {resource_type} resources or differentiation techniques are recommended for adapting a {subject} lesson to meet the needs of a {age_group} student with {sen_type} who is dealing with {focus_point}?",
            # Behavior Management/Policy
            "When a {age_group} student with {sen_type} exhibits {focus_point} during {activity}, what is the recommended school policy or best practice for de-escalation and positive behavior support in a mainstream/SEN school setting?",
            # Parent/Carer Communication
            "How can a teacher best communicate concerns about {focus_point} to the parents/carers of a student with {sen_type} in {age_group}, ensuring a collaborative approach?",
            # Assessment/IEP goals
            "What are measurable and achievable Individual Education Plan (IEP) goals for a {age_group} student with {sen_type} who is currently exhibiting {focus_point} in {subject}?"
        ]

        # **UPDATED: Teacher Focus Points (specific difficulties)**
        self.teacher_focus_points = {
            "ASD": [
                "sensory overload in a busy classroom",
                "difficulty transitioning between subjects/tasks",
                "rigid thinking impacting problem-solving",
                "challenges with non-literal language"
            ],
            "ADHD": [
                "consistent difficulty maintaining focus on multi-step tasks",
                "managing impulsive interruptions during whole-class instruction",
                "organizing materials and completing work on time",
                "fidgeting/motor restlessness distracting other students"
            ],
            "SEMH": [
                "dealing with extreme anxiety preventing participation",
                "responding to non-verbal cues of distress or withdrawal",
                "re-integrating after a significant emotional outburst",
                "building self-esteem in students who fear failure"
            ],
            "SLCN": [
                "supporting understanding of complex instructions in Science",
                "improving oral contribution during group work",
                "scaffolding essay writing for better structure",
                "using alternative communication methods in PE"
            ],
            # Fallback for less detailed categories
            "MLD": ["general academic underachievement", "memory recall challenges"],
            "SPLD": ["decoding and reading fluency", "handwriting and recording work"],
            "PD": ["accessible resources in Art", "managing fatigue during a full school day"],
            "VI": ["adapting visual worksheets in Math", "safe movement around the classroom"],
            "HI": ["ensuring full access to verbal instruction", "using technology to support communication"]
        }

    def generate_llm_responses(self, query, num_responses=4):
        """
        Generate multiple LLM responses for each teacher query.
        Simulated since actual OpenAI API call is not available.
        """
        responses = []

        # Sample response templates for different types of interventions
        response_templates = [
            {
                "type": "Environmental",
                "content": "Create a calm, structured environment with visual supports and clear routines. Use noise-cancelling headphones if needed and provide a designated quiet space for breaks."
            },
            {
                "type": "Instructional",
                "content": "Break tasks into smaller, manageable steps with visual cues. Use multi-sensory teaching approaches and provide frequent positive reinforcement."
            },
            {
                "type": "Social",
                "content": "Implement peer buddy systems and social stories. Practice social skills explicitly and provide opportunities for structured social interaction."
            },
            {
                "type": "Behavioral",
                "content": "Use positive behavior support strategies with clear expectations. Implement a token economy system and teach self-regulation techniques."
            },
            {
                "type": "Assessment",
                "content": "Modify assessment methods using alternative formats. Allow extra time and provide assistive technology where appropriate."
            }
        ]

        # Select appropriate responses based on query content
        selected_responses = random.sample(
            response_templates, min(num_responses, len(response_templates)))

        for i, template in enumerate(selected_responses):
            response = {
                "id": f"response_{i+1}",
                "type": template["type"],
                "content": template["content"],
                # Simulated quality score
                "quality_score": random.uniform(0.6, 0.95)
            }
            responses.append(response)

        return responses

    def create_teacher_query(self, sen_type, age_group, subject):
        """Creates a query that a teacher would realistically ask about an SEN student."""
        template = random.choice(self.teacher_question_templates)
        focus_point = random.choice(self.teacher_focus_points.get(
            sen_type, ["general support needs"]))

        query = template.format(
            sen_type=self.sen_categories[sen_type],
            age_group=age_group,
            subject=subject,
            focus_point=focus_point,
            resource_type=random.choice(
                ["visual", "digital", "kinaesthetic", "low-tech"]),
            activity=random.choice(
                ["group discussion", "independent work", "assessment", "break time"]),
        )

        return {
            "id": f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}",
            "sen_category": sen_type,
            "sen_full_name": self.sen_categories[sen_type],
            "age_group": age_group,
            "subject": subject,
            "teacher_query_text": query,  # Renamed key
            "difficulty_level": random.choice(["Low", "Medium", "High"]),
            "priority": random.choice(["High", "Medium", "Low"])
        }

    def generate_question_set(self, num_questions=20):
        """Generate a set of SEN teacher queries with multiple LLM responses."""
        questions = []

        for i in range(num_questions):
            # Randomly select parameters
            sen_type = random.choice(list(self.sen_categories.keys()))
            age_group = random.choice(self.age_groups)
            subject = random.choice(self.subjects)

            # Create the teacher query instead of a scenario
            query_data = self.create_teacher_query(
                sen_type, age_group, subject)

            # Generate multiple LLM responses (these are the potential answers to the teacher's question)
            llm_responses = self.generate_llm_responses(
                query_data["teacher_query_text"])

            question_data = {
                **query_data,
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
            # Uses 'teacher_query_text' instead of 'scenario_text'
            question_text = f"Question {i}: {question['teacher_query_text']}\n\n"
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

    def export_to_csv(self, questions, filename="sen_survey_teacher_queries.csv"):
        """Export questions to CSV for easy import/reference"""
        rows = []

        for question in questions:
            base_row = {
                "Question_ID": question['id'],
                "SEN_Category": question['sen_category'],
                "Age_Group": question['age_group'],
                "Subject": question['subject'],
                "Teacher_Query": question['teacher_query_text'],  # Renamed key
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
        print(f"Teacher Queries exported to {filename}")
        return filename

    def create_forms_import_file(self, forms_data, filename="microsoft_forms_teacher_queries_import.txt"):
        """Create a text file with formatted questions for Microsoft Forms"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(
                "MICROSOFT FORMS SURVEY QUESTIONS - SEN Teacher Feedback (Queries)\n")
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

# Generate question set (now generating teacher queries)
print("Generating SEN Teacher Queries and suggested answers...")
queries = generator.generate_question_set(
    num_questions=10)  # Start with 10 for testing

print(f"Generated {len(queries)} teacher queries successfully!")

# Show first query as example
if queries:
    print("\nExample Teacher Query:")
    print("-" * 50)
    print(f"Query: {queries[0]['teacher_query_text']}")
    print(f"SEN Category: {queries[0]['sen_full_name']}")
    print(f"Age Group: {queries[0]['age_group']}")
    print(f"Subject: {queries[0]['subject']}")
    print("\nLLM Response Options (Potential Answers):")
    for i, response in enumerate(queries[0]['llm_responses'], 1):
        print(f"{i}. ({response['type']}) {response['content']}")

# 1. Format the data for Microsoft Forms
forms_data = generator.format_for_microsoft_forms(queries)

# 2. Export the data to CSV
generator.export_to_csv(queries)

# 3. Create the text import file for Forms
generator.create_forms_import_file(forms_data)
