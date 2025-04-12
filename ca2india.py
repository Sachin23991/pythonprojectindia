import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for plots
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Load the dataset
df = pd.read_csv("C:/Users/Sachin/Downloads/archive/netflix_titles.csv")
df.head()
df.info()

df.nunique()


print("Summary statistics of numeric columns:\n")
print(df.describe())

missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]
print("Missing values in columns:\n")
print(missing_values)


for col in df.select_dtypes(include='object').columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique value{'s' if unique_count > 1 else ''}")


print(df.columns)


# Shape of the dataset
print("Shape of dataset:", df.shape)

# Data Types of each column
print("\nData Types:\n", df.dtypes)

# Check for missing values
print("\nMissing Values:\n", df.isnull().sum())

# Handling missing values
df['director'] = df['director'].fillna('Not Available')
df['cast'] = df['cast'].fillna('Not Available')
df['country'] = df['country'].fillna('Not Available')
df['date_added'] = df['date_added'].fillna('Not Available')
df['rating'] = df['rating'].fillna('Not Rated')
df['duration'] = df['duration'].fillna('Not Available')

# Convert date_added to datetime
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Extract year and month from 'date_added'
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# Count of each content type
content_type_counts = df['type'].value_counts()

# Define custom colors: Netflix dark red and black
netflix_colors = ['#E50914', '#000000']  # Dark red for 'Movie', black for 'TV Show'

# Plotting content type distribution
plt.figure(figsize=(8, 6))
plt.pie(
    content_type_counts,
    labels=content_type_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=netflix_colors,
    textprops={'color': 'white'}  # White text for better contrast on dark colors
)
plt.title('Distribution of Content Types on Netflix', color='white')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.gca().set_facecolor('#1A1A1A')  # Optional: Set background to dark gray
plt.show()

# Prepare data for titles added per year
titles_per_year = df['year_added'].value_counts().sort_index()
titles_per_year_df = titles_per_year.reset_index()
titles_per_year_df.columns = ['year', 'count']

# Plotting titles added per year
plt.figure(figsize=(12, 6))
sns.barplot(
    data=titles_per_year_df,
    x='year',
    y='count',
    hue='year',             # Assign hue to match x
    palette='viridis',
    legend=False            # Hide the redundant legend
)
plt.title('Number of Titles Added to Netflix Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.show()

# Splitting multiple countries and counting individually
country_counts = df['country'].dropna().str.split(', ').explode().value_counts().head(10)

# Plotting top countries
plt.figure(figsize=(10, 6))
sns.barplot(
    x=country_counts.values,
    y=country_counts.index,
    hue=country_counts.index,        # Added this
    palette='coolwarm',
    legend=False                     # Suppresses extra legend
)
plt.title('Top 10 Countries by Number of Titles')
plt.xlabel('Number of Titles')
plt.ylabel('Country')
plt.show()

# Splitting multiple genres and counting individually
genre_counts = df['listed_in'].str.split(', ').explode().value_counts().head(10)

# Plotting top genres
plt.figure(figsize=(6, 8))
plt.pie(
    genre_counts.values,
    labels=genre_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette('muted')
)
plt.title('Top 10 Most Common Genres on Netflix')
plt.axis('equal')  # Equal aspect ratio makes the pie chart circular
plt.show()

# Count of each rating
rating_counts = df['rating'].value_counts().head(10)

# Plotting rating distribution
plt.figure(figsize=(10, 6))
sns.barplot(
    x=rating_counts.index,
    y=rating_counts.values,
    hue=rating_counts.index,     # Hue same as x to match colors
    palette='pastel',
    legend=False
)
plt.title('Distribution of Content Ratings on Netflix')
plt.xlabel('Rating')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.show()

# Filter only movies
movies_df = df[df['type'] == 'Movie'].copy()

# Clean and extract duration
movies_df = movies_df[movies_df['duration'].str.contains('min', na=False)]
movies_df['duration'] = movies_df['duration'].str.replace(' min', '', regex=False).astype(float)

# Plot movie durations with KDE
plt.figure(figsize=(10, 6))
sns.histplot(data=movies_df, x='duration', bins=30, kde=True, color='coral')
plt.title('Distribution of Movie Durations on Netflix')
plt.xlabel('Duration (minutes)')
plt.ylabel('Number of Movies')
plt.show()
