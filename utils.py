def calculate_bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight (ওজন কম)"
    elif 18.5 <= bmi <= 24.9:
        return "Normal (স্বাভাবিক ওজন)"
    elif 25 <= bmi <= 29.9:
        return "Overweight (অতিরিক্ত ওজন)"
    else:
        return "Obese (স্থূলতা)"

def check_pulse_status(bpm):
    if 60 <= bpm <= 100:
        return "Normal"
    return "Abnormal"
