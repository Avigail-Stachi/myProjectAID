import csv


def load_cases_from_csv(file_path):
    cases = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            case_name, case_instructions = row
            cases[case_name] = case_instructions
    return cases


file_path = r"C:\project\first_aid_treat_fix.csv"
first_aid_cases = load_cases_from_csv(file_path)


def what_to_do(case):
    print(first_aid_cases[case])


what_to_do("fractures")
