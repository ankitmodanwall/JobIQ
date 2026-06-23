def predict_salary(experience):
    """
    Simple salary prediction without ML
    """
    # Base salary + experience increment
    base_salary = 50000
    increment_per_year = 15000
    return base_salary + (experience * increment_per_year)