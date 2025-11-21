# Complete SEN Teacher Query and LLM Answer Generator for Microsoft Forms Survey
import json
import csv
import random
from datetime import datetime
import pandas as pd


class SENQuestionGenerator:
    def __init__(self, openai_api_key=None):
        self.openai_api_key = openai_api_key

        # SEN Categories from UK Education System
        self.sen_categories = {
            "ASD": "Autism Spectrum Disorder", "ADHD": "Attention Deficit Hyperactivity Disorder",
            "SEMH": "Social, Emotional, Mental Health", "SLCN": "Speech, Language, Communication Needs",
            "MLD": "Moderate Learning Difficulties", "SPLD": "Specific Learning Difficulties",
            "PD": "Physical Disability", "VI": "Visual Impairment", "HI": "Hearing Impairment"
        }
        self.age_groups = ["Early Years (3-5)", "Key Stage 1 (5-7)",
                           "Key Stage 2 (7-11)", "Key Stage 3 (11-14)", "Key Stage 4 (14-16)"]
        self.subjects = ["Mathematics", "English", "Science",
                         "Art", "PE", "Social Skills", "Life Skills"]

        # **UPDATED: Teacher Question Templates**
        self.teacher_question_templates = [
            "A teacher has a {age_group} student with {sen_type} struggling with {subject}. What are the **three most effective, quick-to-implement** intervention strategies for this specific {focus_point}?",
            "What specific {resource_type} resources or differentiation techniques are recommended for adapting a {subject} lesson to meet the needs of a {age_group} student with {sen_type} who is dealing with {focus_point}?",
            "When a {age_group} student with {sen_type} exhibits {focus_point} during {activity}, what is the recommended school policy or best practice for de-escalation and positive behavior support in a mainstream/SEN school setting?",
            "How can a teacher best communicate concerns about {focus_point} to the parents/carers of a student with {sen_type} in {age_group}, ensuring a collaborative approach?",
            "What are measurable and achievable Individual Education Plan (IEP) goals for a {age_group} student with {sen_type} who is currently exhibiting {focus_point} in {subject}?"
        ]

        # **UPDATED: Teacher Focus Points (specific difficulties)**
        self.teacher_focus_points = {
            "ASD": ["sensory overload in a busy classroom", "difficulty transitioning between subjects/tasks", "rigid thinking impacting problem-solving"],
            "ADHD": ["consistent difficulty maintaining focus on multi-step tasks", "managing impulsive interruptions during whole-class instruction", "fidgeting/motor restlessness distracting other students"],
            "SEMH": ["dealing with extreme anxiety preventing participation", "responding to non-verbal cues of distress or withdrawal", "re-integrating after a significant emotional outburst"],
            "SLCN": ["supporting understanding of complex instructions in Science", "improving oral contribution during group work", "scaffolding essay writing for better structure"],
            "MLD": ["general academic underachievement", "memory recall challenges"],
            "SPLD": ["decoding and reading fluency", "handwriting and recording work"],
            "PD": ["accessible resources in Art", "managing fatigue during a full school day"],
            "VI": ["adapting visual worksheets in Math", "safe movement around the classroom"],
            "HI": ["ensuring full access to verbal instruction", "using technology to support communication"]
        }

    def get_responses_from_llm(self, query_text, model_name, num_responses=4):
        """
        Simulates generating multiple LLM responses for a query using a specific model.
        (This method contains the logic you would replace with actual API calls.)
        """
        responses = []

        # Define model-specific response variations (simulated)
        if "GPT" in model_name:
            response_types = ["Instructional",
                              "Social", "Environmental", "Behavioral"]
        elif "Gemini" in model_name:
            response_types = ["Behavioral",
                              "Assessment", "Instructional", "Social"]
        elif "Llama" in model_name:
            response_types = ["Environmental",
                              "Instructional", "Social", "Behavioral"]
        elif "Mistral" in model_name:
            response_types = ["Behavioral",
                              "Environmental", "Instructional", "Social"]
        else:
            response_types = ["Instructional",
                              "Environmental", "Social", "Behavioral"]

        # Ensure we use exactly num_responses types
        response_types = response_types[:num_responses]

        # Template content based on type (prepended with model name for tracking)
        response_templates = {
            "Environmental": f"({model_name}) Structure the learning space; provide a quiet corner, use visual timetables, and ensure minimal clutter to manage sensory input.",
            "Instructional": f"({model_name}) Simplify instructions into visual, multi-step checklists. Use immediate, frequent positive reinforcement tied to effort, not just outcome.",
            "Social": f"({model_name}) Implement a structured peer-buddy system specific to the activity. Role-play social interactions and use brief 'social stories' before lessons.",
            "Behavioral": f"({model_name}) Establish clear, co-created classroom rules. Use a points/token system focused on self-regulation and impulse control, with specific, non-judgmental feedback.",
            "Assessment": f"({model_name}) Use alternative assessment formats (e.g., oral presentation, video recording) and focus IEP goals on functional skills development rather than pure academic metrics."
        }

        selected_types = random.sample(
            response_types, min(num_responses, len(response_types)))

        for i, type_name in enumerate(selected_types):
            response = {
                "id": f"{model_name}_{i+1}",
                "type": type_name,
                "content": response_templates.get(type_name, f"({model_name}) Default strategy content."),
                "quality_score": random.uniform(0.7, 0.95) if "GPT" in model_name else random.uniform(0.6, 0.9)
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
            "teacher_query_text": query,
            "difficulty_level": random.choice(["Low", "Medium", "High"]),
            "priority": random.choice(["High", "Medium", "Low"])
        }

    def generate_question_set(self, num_queries=25,
                              models=["GPT-4o", "Gemini 25 Pro", "Llama 3", "Mistral Large"]):
        """
        Generates a set of teacher queries, with each query answered by multiple LLMs.
        """
        all_data = []

        for i in range(num_queries):
            # 1. Select parameters and create the core query
            sen_type = random.choice(list(self.sen_categories.keys()))
            age_group = random.choice(self.age_groups)
            subject = random.choice(self.subjects)
            query_data = self.create_teacher_query(
                sen_type, age_group, subject)

            model_responses = {}

            # 2. Generate responses from EACH model
            for model in models:
                responses = self.get_responses_from_llm(
                    query_data["teacher_query_text"], model)
                model_responses[model] = responses

            # 3. Compile the final structured data
            question_data = {
                **query_data,
                "all_model_responses": model_responses,
                "created_date": datetime.now().isoformat()
            }

            all_data.append(question_data)

        return all_data

    def format_for_microsoft_forms(self, questions, default_model_for_options="GPT-4o"):
        """
        Format questions for easy copy-paste into Microsoft Forms.
        Uses responses from the specified default model for the multiple-choice options.
        """
        forms_data = []

        for i, question in enumerate(questions, 1):
            question_text = f"Question {i}: {question['teacher_query_text']}\n\n"
            question_text += f"SEN Category: {question['sen_full_name']}\n"
            question_text += f"Age Group: {question['age_group']}\n"
            question_text += f"Subject: {question['subject']}\n\n"
            question_text += "Please select the BEST response from the options below, or choose 'Other' to provide your own improved answer:"

            options_responses = question['all_model_responses'].get(
                default_model_for_options, [])

            options = []
            for j, response in enumerate(options_responses, 1):
                # We rename the option to obscure the model source for the survey
                option_text = f"Option {j} (Focus: {response['type']}): {response['content']}"
                options.append(option_text)

            options.append(
                "Other (Please specify your improved response in the text box below)")

            forms_data.append({
                "question_number": i,
                "question_text": question_text,
                "options": options,
                "follow_up_text": "If you selected 'Other', please provide your improved response:",
                "metadata": {
                    "options_source_model": default_model_for_options
                }
            })

        return forms_data

    def export_to_csv(self, questions, filename="sen_survey_teacher_queries_multi_model.csv"):
        """
        Export questions to CSV, flattening the nested responses from multiple models.
        """
        rows = []
        if not questions:
            return filename

        models = list(questions[0]['all_model_responses'].keys())
        num_responses_per_model = len(
            list(questions[0]['all_model_responses'].values())[0])

        for question in questions:
            base_row = {
                "Question_ID": question['id'],
                "SEN_Category": question['sen_category'],
                "Age_Group": question['age_group'],
                "Subject": question['subject'],
                "Teacher_Query": question['teacher_query_text'],
                "Difficulty_Level": question['difficulty_level'],
                "Created_Date": question['created_date']
            }

            # Add data for each model and its responses
            for model_name in models:
                responses = question['all_model_responses'].get(model_name, [])
                model_prefix = model_name.replace(
                    ' ', '_').replace('.', '').replace('-', '')

                for i in range(num_responses_per_model):
                    if i < len(responses):
                        response = responses[i]
                        prefix = f"{model_prefix}_Response_{i+1}"
                        base_row[f"{prefix}_Type"] = response['type']
                        base_row[f"{prefix}_Content"] = response['content']
                        base_row[f"{prefix}_Quality"] = response['quality_score']
                    # Else: columns are left blank if no response was generated (handled by DataFrame creation)

            rows.append(base_row)

        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
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
            f.write(
                "4. Ensure the source model for the options is noted in the Form's description/metadata.\n")
            f.write(
                "5. Add a text box after each multiple choice for detailed feedback on the 'Other' option.\n\n")
            f.write("="*60 + "\n\n")

            for question_data in forms_data:
                f.write(f"QUESTION {question_data['question_number']}:\n")
                f.write("-" * 40 + "\n")
                f.write(f"{question_data['question_text']}\n\n")

                f.write("OPTIONS (Source Model: {})\n".format(
                    question_data['metadata']['options_source_model']))
                for i, option in enumerate(question_data['options'], 1):
                    f.write(f"{i}. {option}\n")

                f.write(
                    f"\nFOLLOW-UP TEXT BOX: {question_data['follow_up_text']}\n")
                f.write("\n" + "="*60 + "\n\n")

        return filename

# --- Execution Block ---


# Initialize the generator
generator = SENQuestionGenerator()

# Define models and number of queries (You can easily change these variables here)
MODELS = ["GPT-4o", "Gemini 25 Pro", "Llama 3", "Mistral Large"]
NUM_QUERIES = 25

print(
    f"Generating {NUM_QUERIES} unique Teacher Queries, answered by {len(MODELS)} distinct LLMs...")
queries = generator.generate_question_set(
    num_queries=NUM_QUERIES,
    models=MODELS
)

# 1. Format the data for Microsoft Forms (using GPT-4o responses as the options)
forms_data = generator.format_for_microsoft_forms(
    queries, default_model_for_options="GPT-4o")

# 2. Export the full data to CSV (for analysis)
csv_filename = generator.export_to_csv(queries)

# 3. Create the text import file for Forms (for survey creation)
forms_filename = generator.create_forms_import_file(forms_data)

print("\n--- Generation Complete ---")
print(f"Total base queries generated: {len(queries)}")
print(f"Total responses for analysis: {len(queries) * len(MODELS) * 4}")
print(f"CSV file created for full data analysis: {csv_filename}")
print(f"Text file created for Microsoft Forms import: {forms_filename}")

# Display a single question example using the NEW key 'all_model_responses'
if queries:
    print("\nExample Query (from the set):")
    q = queries[0]
    print("-" * 50)
    print(f"Query: {q['teacher_query_text']}")
    print(f"Age Group: {q['age_group']} | Subject: {q['subject']}")
    print("\nResponses from all 4 Models:")
    # This loop now correctly iterates over the models and their responses
    for model_name, responses in q['all_model_responses'].items():
        print(f"  > {model_name} Responses:")
        for i, r in enumerate(responses, 1):
            print(f"    - Option {i} ({r['type']}): {r['content'][:60]}...")
