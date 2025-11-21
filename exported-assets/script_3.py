# Create a comprehensive setup guide for Microsoft Forms
def create_microsoft_forms_setup_guide():
    guide = """
# COMPLETE MICROSOFT FORMS SETUP GUIDE FOR SEN SURVEY

## STEP 1: Create the Microsoft Form
1. Go to https://forms.office.com
2. Click "New Form"
3. Title: "SEN Teaching Strategies - Teacher Feedback Survey"
4. Description: "Help us improve AI responses for Special Educational Needs support by evaluating and enhancing these teaching scenarios."

## STEP 2: Form Structure
For each question, follow this format:

### Question Type: Multiple Choice + Text
- **Allow multiple selection**: NO
- **Required**: YES  
- **Add 'Other' option**: YES
- **Follow with Text question**: YES (for improvements)

### Question Format Example:
**Title**: "Scenario 1: [Scenario Text]"
**Subtitle**: "SEN Category: [Category] | Age: [Age Group] | Subject: [Subject]"
**Question**: "Which response would be most effective? Select the best option or choose 'Other' to provide your own approach."

**Options**:
□ Environmental Approach: [Response text]
□ Instructional Approach: [Response text]  
□ Social Approach: [Response text]
□ Behavioral Approach: [Response text]
□ Other (specify below)

**Follow-up Text Box**:
"If you selected 'Other' or want to improve any response, please provide your enhanced approach:"

## STEP 3: Advanced Features
- **Add branching**: Route teachers to additional questions based on their expertise
- **Set response collection**: Limit to organization members for data quality
- **Enable response summary**: Allow teachers to see anonymized results
- **Add thank you message**: Include timeline for sharing improved AI responses

## STEP 4: Distribution Strategy
- **Share via email**: Send to SEN coordinators and subject leads
- **Embed in platform**: Add to school intranet or learning management system
- **QR code**: Create for easy mobile access during staff meetings
- **Reminder system**: Set up follow-up emails through Power Automate

## STEP 5: Data Collection Best Practices
- **Pilot test**: Run with 3-5 teachers first
- **Collect demographic info**: Teaching experience, SEN specialization, subjects taught
- **Set collection period**: 2-3 weeks for adequate response rate
- **Monitor responses**: Check daily for technical issues or unclear questions

## STEP 6: Response Analysis Setup (Power Automate)
1. Create automated flow: "When a new response is submitted"
2. Get response details from your form
3. Parse responses into categories
4. Store in Excel Online or SharePoint List
5. Send summary emails to research team

## STEP 7: Data Processing for AI Training
After collection:
- Export responses to Excel
- Categorize teacher improvements by intervention type
- Create preference pairs (Original LLM vs Teacher Enhanced)
- Format for RLHF training dataset
- Anonymize all teacher identifiers

## POWER AUTOMATE WORKFLOW TEMPLATE
```
Trigger: When a new response is submitted
├── Get response details
├── Parse JSON responses
├── Create Excel row with structured data
├── Send confirmation email to respondent
└── Notify research team of new response
```

## SAMPLE DATA STRUCTURE FOR ANALYSIS
| ResponseID | TeacherID | ScenarioID | SENCategory | SelectedOption | TeacherImprovement | Confidence | Timestamp |
|------------|-----------|------------|-------------|-----------------|-------------------|------------|-----------|
| R001       | T_ANON_01 | S_001      | ADHD        | Environmental   | "Add fidget tools" | High       | 2025-10-28 |

This structure enables both quantitative analysis (which options chosen most) and qualitative analysis (teacher improvements for AI training).
"""
    return guide

# Save the setup guide
setup_guide = create_microsoft_forms_setup_guide()
with open("microsoft_forms_complete_setup_guide.txt", "w", encoding="utf-8") as f:
    f.write(setup_guide)

print("Complete Microsoft Forms setup guide created!")
print("\nSetup Summary:")
print("1. ✓ Generated SEN scenarios with multiple LLM responses")
print("2. ✓ Formatted questions for Microsoft Forms")  
print("3. ✓ Created CSV reference file for data tracking")
print("4. ✓ Generated import template for easy form creation")
print("5. ✓ Created complete setup guide with Power Automate workflow")
print("6. ✓ Included data analysis structure for AI training")

print(f"\nFiles created:")
print(f"- sen_survey_questions.csv (reference data)")
print(f"- microsoft_forms_import.txt (copy-paste questions)")
print(f"- microsoft_forms_complete_setup_guide.txt (full instructions)")

# Create a final validation check
print(f"\nValidation Check:")
print(f"- Total scenarios generated: {len(questions)}")
print(f"- SEN categories covered: {len(set(q['sen_category'] for q in questions))}")
print(f"- Age groups covered: {len(set(q['age_group'] for q in questions))}")
print(f"- Subjects covered: {len(set(q['subject'] for q in questions))}")
print(f"- Average responses per scenario: {sum(len(q['llm_responses']) for q in questions) / len(questions):.1f}")

print("\n🎯 Ready for Microsoft Forms deployment!")
print("Next steps:")
print("1. Open microsoft_forms_complete_setup_guide.txt")
print("2. Follow the step-by-step instructions")
print("3. Copy questions from microsoft_forms_import.txt")
print("4. Set up Power Automate workflow for data collection")
print("5. Distribute survey to teachers")
print("6. Analyze responses for AI training data")