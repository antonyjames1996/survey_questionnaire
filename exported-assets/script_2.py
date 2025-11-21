# Add advanced features to the generator
class AdvancedSENSurveyManager:
    def __init__(self, generator):
        self.generator = generator
        
    def create_response_analysis_template(self):
        """Create template for analyzing teacher responses"""
        analysis_template = {
            "response_categories": {
                "Environmental": "Modifications to physical/sensory environment",
                "Instructional": "Teaching methods and curriculum adaptations", 
                "Social": "Peer interaction and social skills support",
                "Behavioral": "Behavior management and self-regulation",
                "Assessment": "Alternative assessment and evaluation methods",
                "Technology": "Assistive technology and digital tools",
                "Communication": "Language and communication support",
                "Other": "Teacher-generated innovative approaches"
            },
            "quality_metrics": [
                "Evidence-based approach",
                "Practical implementation",
                "Student-centered focus",
                "Differentiation level",
                "Collaboration consideration",
                "Long-term sustainability"
            ],
            "data_collection_fields": [
                "selected_option",
                "teacher_improvement", 
                "confidence_level",
                "implementation_feasibility",
                "additional_resources_needed"
            ]
        }
        return analysis_template
    
    def generate_power_automate_workflow(self):
        """Generate Power Automate workflow instructions for Microsoft Forms"""
        workflow_steps = {
            "workflow_name": "SEN Survey Response Processing",
            "trigger": "When a new response is submitted (Microsoft Forms)",
            "actions": [
                {
                    "step": 1,
                    "action": "Get response details",
                    "description": "Extract all form responses including multiple choice and text answers"
                },
                {
                    "step": 2, 
                    "action": "Parse responses",
                    "description": "Categorize responses by SEN type, selected options, and improvements"
                },
                {
                    "step": 3,
                    "action": "Add to Excel/SharePoint",
                    "description": "Store responses in structured format for analysis"
                },
                {
                    "step": 4,
                    "action": "Send confirmation email",
                    "description": "Thank teachers and provide timeline for results sharing"
                }
            ],
            "data_structure": {
                "response_id": "Unique identifier for each response",
                "teacher_id": "Anonymous teacher identifier", 
                "question_id": "Links to original scenario",
                "selected_option": "Which LLM response was chosen",
                "improvement_text": "Teacher's enhanced response",
                "rating_score": "Quality rating of original responses",
                "submission_timestamp": "When response was submitted"
            }
        }
        return workflow_steps
    
    def create_batch_scenarios(self, sen_focus=None, age_focus=None, quantity=50):
        """Generate larger batches of scenarios for comprehensive surveys"""
        if sen_focus:
            # Focus on specific SEN categories
            focused_categories = [sen_focus] if isinstance(sen_focus, str) else sen_focus
        else:
            focused_categories = list(self.generator.sen_categories.keys())
            
        if age_focus:
            focused_ages = [age_focus] if isinstance(age_focus, str) else age_focus
        else:
            focused_ages = self.generator.age_groups
            
        scenarios = []
        scenarios_per_combo = max(1, quantity // (len(focused_categories) * len(focused_ages)))
        
        for sen_type in focused_categories:
            for age_group in focused_ages:
                for _ in range(scenarios_per_combo):
                    subject = random.choice(self.generator.subjects)
                    scenario = self.generator.create_scenario(sen_type, age_group, subject)
                    scenario['llm_responses'] = self.generator.generate_llm_responses(scenario['scenario_text'])
                    scenarios.append(scenario)
        
        return scenarios[:quantity]  # Trim to exact quantity requested

# Create advanced manager
advanced_manager = AdvancedSENSurveyManager(generator)

# Generate analysis template
analysis_template = advanced_manager.create_response_analysis_template()
print("Response Analysis Categories:")
for category, description in analysis_template['response_categories'].items():
    print(f"- {category}: {description}")

# Generate Power Automate workflow
workflow = advanced_manager.generate_power_automate_workflow()
print(f"\n{workflow['workflow_name']} Steps:")
for action in workflow['actions']:
    print(f"{action['step']}. {action['action']}: {action['description']}")

# Create a focused batch (example: ADHD scenarios for primary age)
print("\nGenerating focused batch of scenarios...")
focused_scenarios = advanced_manager.create_batch_scenarios(
    sen_focus=["ADHD", "ASD"], 
    age_focus=["Key Stage 1 (5-7)", "Key Stage 2 (7-11)"],
    quantity=15
)

print(f"Generated {len(focused_scenarios)} focused scenarios")
print(f"First focused scenario: {focused_scenarios[0]['scenario_text'][:100]}...")