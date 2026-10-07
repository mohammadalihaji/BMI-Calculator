# bmi_cli.py

def get_positive_float(prompt):
    """Repeatedly prompts the user until a valid, positive float is entered."""
    while True:
        user_input = input(prompt).strip()
        try:
            value = float(user_input)
            if value <= 0:
                print("Error: Value must be greater than 0. Please try again.\n")
                continue
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a valid numerical value.\n")


def calculate_bmi(weight, height):
    """Calculates BMI: weight (kg) / (height (m) ** 2)"""
    return weight / (height ** 2)


def get_bmi_category(bmi):
    """Returns the WHO classification category for a given BMI."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main():
    print("=" * 40)
    print("       BODY MASS INDEX (BMI) CALCULATOR       ")
    print("=" * 40)

    # 1. Safely retrieve validated inputs
    weight = get_positive_float("Enter your weight in kg (e.g., 70): ")
    height = get_positive_float("Enter your height in meters (e.g., 1.75): ")

    # 2. Calculate BMI
    bmi = calculate_bmi(weight, height)

    # 3. Determine category
    category = get_bmi_category(bmi)

    # 4. Display result
    print("\n" + "-" * 40)
    print(f"Your BMI:      {bmi:.2f}")
    print(f"Health Status: {category}")
    print("-" * 40)


if __name__ == "__main__":
    main()
