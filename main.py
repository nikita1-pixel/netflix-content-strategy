import pandas as pd

df = pd.read_csv(
    r"C:\Users\nirma\OneDrive\Desktop\Data Analyst\Netflix_analysis\mymoviedb.csv",
    lineterminator = "\n",
    on_bad_lines = 'skip'
)
df['Movie_ID'] = df.index + 1
print("Formatting dates...")
df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors ='coerce')

print('Buildinf dim_movie.csv')
movies_df = df[['Movie_ID', 'Title', 'Release_Date', 'Popularity', 'Vote_Count', 'Vote_Average', 'Original_Language', 'Poster_Url', 'Overview']].copy()

movies_df['Overview'] = movies_df['Overview'].astype(str).str.replace(r'\n|\r', ' ', regex=True)
movies_df['Title'] = movies_df['Title'].astype(str).str.replace(r'\n|\r', ' ', regex=True)
movies_df.to_csv("dim_movies.csv", index = False)

print ("Normalizing Genres....")
df['Genre'] = df['Genre'].astype(str).str.split(', ')
genre_exploaded = df[['Movie_ID', 'Genre']].explode('Genre')
genre_exploaded['Genre'] = genre_exploaded['Genre'].str.strip()

unique_genres = pd.DataFrame(genre_exploaded['Genre'].dropna().unique(), columns = ['Genre_Name'])
unique_genres['Genre_ID'] = unique_genres.index + 1
unique_genres.to_csv("dim_genres.csv", index = False)
print("Building dim_movie_genres.csv...")

fact_genres = genre_exploaded.merge(unique_genres, left_on ='Genre', right_on ='Genre_Name', how = 'inner')
fact_genres = fact_genres[['Movie_ID', 'Genre_ID']]
fact_genres.to_csv("Fact_movie_genres.csv", index = False)
print("Building fact_movie_genres.csv.....")


print("\nSUCCESS: Data engineering completed! Check")