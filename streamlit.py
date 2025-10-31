import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Census Data Analysis", layout="wide")

# --- Title and Intro ---
st.title("📊 Census Data Analysis Dashboard By Donthireddy Rakshitha")
st.write("Upload your Census CSV file and explore insights interactively with collapsible sections.")

# --- File Uploader ---
uploaded_file = st.file_uploader("📂 Upload your census.csv file", type=["csv"])

if uploaded_file is not None:
    census = pd.read_csv(uploaded_file)
    st.success("✅ Dataset loaded successfully!")
    st.dataframe(census.head())

    st.divider()
    st.subheader("🔍 Choose an Analysis to View:")

    # ------------------- ANALYSIS SECTIONS -------------------

    with st.expander("1️⃣ Senior Citizens to be added in next X years"):
        X = st.number_input("Enter number of years", min_value=1, max_value=50, value=5)
        senior_voters = census[(census['Age'] < 60) & ((census['Age'] + X) >= 60)]
        st.success(f"Number of Senior Citizens to be added in next {X} years: **{len(senior_voters)}**")

    with st.expander("2️⃣ Voters to be added in next X years"):
        X = st.number_input("Enter number of years", min_value=1, max_value=50, value=5, key="voters")
        new_voters = census[(census['Age'] < 18) & ((census['Age'] + X) >= 18)]
        st.info(f"Number of voters to be added in next {X} years: **{len(new_voters)}**")

    with st.expander("3️⃣ Employable Female Citizens (Widowed / Divorced)"):
        employable_females = census[
            (census['Gender'] == 'Female') &
            (census['Marital Status'].isin(['Widowed', 'Divorced'])) &
            (census['Weeks Worked'] != 0)
        ]
        st.success(f"Number of Employable Female Citizens: **{len(employable_females)}**")
        st.dataframe(employable_females[['Age', 'Gender', 'Marital Status', 'Weeks Worked']].head())

    with st.expander("4️⃣ Orphans for each category (Parents Present)"):
        st.bar_chart(census['Parents Status'].value_counts())

    with st.expander("5️⃣ Pension Additions after X years"):
        X = st.number_input("Enter number of years", min_value=1, max_value=50, value=5, key="pension")
        pension_add = census.loc[(census['Age'] < 60) & (census['Age'] + X >= 60)].shape[0]
        st.write(f"Pensioners to be added in {X} years: **{pension_add}**")

    with st.expander("6️⃣ Gender-wise Per Capita Income"):
        gender_pci = census.groupby('Gender')['Income'].sum() / census['Gender'].value_counts()
        st.dataframe(gender_pci)

    with st.expander("7️⃣ Overall Per Capita Income"):
        st.write(f"Per Capita Income: **{census['Income'].mean():,.2f}**")

    with st.expander("8️⃣ Total Tax to be Collected (10%)"):
        tax_collected = (census['Income'] * 0.1).sum()
        st.write(f"Total Tax: **{tax_collected:,.2f}**")

    # --- Newly Added Section ---
    with st.expander("9️⃣ Total Income of Different Types of Tax Payers"):
        if 'Taxfilter status' in census.columns:
            total_income = census.groupby('Taxfilter status')['Income'].sum().reset_index()
            total_income['Total Tax (10%)'] = total_income['Income'] * 0.10
            st.write("### 💰 Total Income and Tax by Taxpayer Type")
            st.dataframe(total_income)
        else:
            st.warning("⚠️ 'Taxfilter status' column not found in dataset.")

    with st.expander("🔟 Gender-wise Total Income"):
        st.bar_chart(census.groupby('Gender')['Income'].sum())

    with st.expander("1️⃣1️⃣ Sex Ratio (Male : Female)"):
        gender_count = census['Gender'].value_counts()
        if 'Male' in gender_count and 'Female' in gender_count:
            sex_ratio = gender_count['Male'] / gender_count['Female']
            st.write(f"Sex Ratio = **{sex_ratio:.2f} : 1**")
        else:
            st.warning("Not enough gender data to calculate ratio.")

    with st.expander("1️⃣2️⃣ Education vs Employment"):
        edu_employment = census.groupby(['Education', 'Weeks Worked']).size().reset_index(name='Count')
        st.dataframe(edu_employment)

    with st.expander("1️⃣3️⃣ Education & Gender-wise Count"):
        education_gender = census.groupby(['Education', 'Gender']).size().reset_index(name='Count')
        st.dataframe(education_gender)

    with st.expander("1️⃣4️⃣ Widow Female Count"):
        widow_female = census[(census['Gender'] == 'Female') & (census['Marital Status'] == 'Widowed')]
        st.write(f"No. of Widow Females: **{len(widow_female)}**")

    with st.expander("1️⃣5️⃣ Parents Status & Gender-wise Count"):
        parent = census.groupby(['Parents Status', 'Gender']).size().reset_index(name='Count')
        st.dataframe(parent)

    with st.expander("1️⃣6️⃣ Citizens aged above 60 (by Citizenship)"):
        age_60 = census[census['Age'] > 60].groupby('Citizen Ship').size().reset_index(name='Count')
        st.dataframe(age_60)

    with st.expander("1️⃣7️⃣ Employable Widows & Divorced (All Genders)"):
        employable = census[
            (census['Marital Status'].isin(['Widowed', 'Divorced'])) &
            (census['Weeks Worked'] != 0)
        ]
        st.write(f"Total Employable Widows/Divorced: **{len(employable)}**")

    with st.expander("1️⃣8️⃣ Non-citizens Working Percentage"):
        non_citizens = census[census['Citizen Ship'] == 'Foreignborn-NotacitizenofUS']
        percent_working = (non_citizens['Weeks Worked'] > 0).mean() * 100
        st.write(f"Working Non-citizens: **{percent_working:.2f}%**")

    with st.expander("1️⃣9️⃣ Money Generated by Non-citizens"):
        non_citizens = census[census['Citizen Ship'] == 'Foreignborn-NotacitizenofUS']
        money_generated = non_citizens['Income'].sum()
        st.write(f"Total Income of Non-citizens: **{money_generated:,.2f}**")

    with st.expander("2️⃣0️⃣ Citizens above 23 with No Employment (Doctorate Holders)"):
        filtered = census[
            (census['Age'] > 23) &
            (census['Weeks Worked'] == 0) &
            (census['Education'] == 'Doctoratedegree(PhDEdD)')
        ][['Age', 'Weeks Worked', 'Education']]
        st.dataframe(filtered)

else:
    st.warning("👆 Please upload a CSV file to begin.")
