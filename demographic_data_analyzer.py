import pandas as pd

def calculate_demographic_data(print_data=True):
    # Sample dataset
    data = {
        'age': [39, 50, 38, 53, 28],
        'workclass': ['State-gov', 'Self-emp-not-inc', 'Private', 'Private', 'Private'],
        'fnlwgt': [77516, 83311, 215646, 234721, 338409],
        'education': ['Bachelors', 'Bachelors', 'HS-grad', '11th', 'Bachelors'],
        'education-num': [13, 13, 9, 7, 13],
        'marital-status': ['Never-married', 'Married-civ-spouse', 'Divorced', 'Married-civ-spouse', 'Married-civ-spouse'],
        'occupation': ['Adm-clerical', 'Exec-managerial', 'Handlers-cleaners', 'Handlers-cleaners', 'Prof-specialty'],
        'relationship': ['Not-in-family', 'Husband', 'Not-in-family', 'Husband', 'Wife'],
        'race': ['White', 'White', 'White', 'Black', 'Black'],
        'sex': ['Male', 'Male', 'Male', 'Male', 'Female'],
        'capital-gain': [2174, 0, 0, 0, 0],
        'capital-loss': [0, 0, 0, 0, 0],
        'hours-per-week': [40, 13, 40, 40, 40],
        'native-country': ['United-States', 'United-States', 'United-States', 'United-States', 'Cuba'],
        'salary': ['<=50K', '<=50K', '<=50K', '<=50K', '<=50K']
    }

    df = pd.DataFrame(data)

    # Clean whitespace
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # 1. Race count
    race_count = df['race'].value_counts()

    # 2. Average age of men
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage with Bachelors degree
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # 4. Higher vs lower education
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    higher_education_rich = round((df[higher_education]['salary'] == '>50K').mean() * 100, 1)
    lower_education_rich = round((df[lower_education]['salary'] == '>50K').mean() * 100, 1)

    # 5. Minimum work hours
    min_work_hours = df['hours-per-week'].min()

    # 6. Rich among those who work minimum hours
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round((num_min_workers['salary'] == '>50K').mean() * 100, 1)

    # 7. Country with highest percentage of rich people
    country_earning = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_total = df['native-country'].value_counts()
    country_percentage = (country_earning / country_total * 100).dropna()

    if not country_percentage.empty:
        highest_earning_country = country_percentage.idxmax()
        highest_earning_country_percentage = round(country_percentage.max(), 1)
    else:
        highest_earning_country = "No data"
        highest_earning_country_percentage = 0

    # 8. Top occupation for >50K earners in India
    india_rich_jobs = df[
        (df['native-country'] == 'India') & (df['salary'] == '>50K')
    ]['occupation']
    top_IN_occupation = india_rich_jobs.value_counts().idxmax() if not india_rich_jobs.empty else "No data"

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print("Highest percentage of rich people in country:", highest_earning_country_percentage)
        print("Top occupations in India for >50K earners:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
