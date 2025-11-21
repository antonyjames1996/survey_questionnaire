# Format for Microsoft Forms and create export files
print("Formatting questions for Microsoft Forms...")
forms_data = generator.format_for_microsoft_forms(questions)

# Export to CSV for reference
csv_filename = generator.export_to_csv(questions)

# Create Microsoft Forms import file
forms_filename = generator.create_forms_import_file(forms_data)

print(f"\nFiles created:")
print(f"1. CSV Reference: {csv_filename}")
print(f"2. Microsoft Forms Import: {forms_filename}")

# Show formatted example for Microsoft Forms
print("\nExample Microsoft Forms Question Format:")
print("="*60)
print(forms_data[0]['question_text'])
print("\nOptions to add in Microsoft Forms:")
for i, option in enumerate(forms_data[0]['options'], 1):
    print(f"{i}. {option}")
print(f"\nFollow-up text box: {forms_data[0]['follow_up_text']}")