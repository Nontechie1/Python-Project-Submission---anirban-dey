import pandas as pd
import sys
from typing import List, Dict


class MovieRecommender:
    def __init__(self, csv_file: str):
        """Initialize the MovieRecommender with a CSV file."""
        try:
            self.df = pd.read_csv(csv_file)
            # Clean genre data by splitting and flattening
            self.df['genre'] = self.df['genre'].str.split(', ')
            # Create a list of unique genres
            self.available_genres = sorted(list(set([
                genre
                for genres in self.df['genre'].dropna()
                for genre in genres
            ])))
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            sys.exit(1)

    def get_available_genres(self) -> List[str]:
        """Return list of available genres."""
        return self.available_genres

    def recommend_movies(self, selected_genre: str, limit: int = 5) -> List[Dict]:
        """Recommend movies based on genre."""
        try:
            # Filter movies that contain the selected genre
            filtered_movies = self.df[self.df['genre'].apply(
                lambda x: selected_genre in x if isinstance(x, list) else False
            )]

            # Sort by rating and get top movies
            top_movies = filtered_movies.nlargest(limit, 'avg_vote')

            # Convert to list of dictionaries
            recommendations = top_movies[[
                'original_title', 'year', 'avg_vote', 'description']].to_dict('records')
            return recommendations

        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []


def main():
    """Main function to run the movie recommender."""
    try:
        # Initialize recommender
        recommender = MovieRecommender('movies.csv')

        # Display available genres
        print("\nAvailable genres:")
        for i, genre in enumerate(recommender.get_available_genres(), 1):
            print(f"{i}. {genre}")

        # Get user input
        while True:
            try:
                genre_choice = input(
                    "\nEnter a genre from the list above: ").strip()
                if genre_choice in recommender.get_available_genres():
                    break
                else:
                    print("Invalid genre. Please choose from the available list.")
            except Exception as e:
                print(f"Error processing input: {str(e)}")

        # Get recommendations
        recommendations = recommender.recommend_movies(genre_choice)

        # Display recommendations
        if recommendations:
            print(f"\nTop 5 {genre_choice} movies:")
            print("-" * 80)
            for i, movie in enumerate(recommendations, 1):
                print(f"{i}. {movie['original_title']} ({movie['year']})")
                print(f"   Rating: {movie['avg_vote']}/10")
                print(f"   Description: {movie['description']}")
                print("-" * 80)
        else:
            print(f"No movies found for genre: {genre_choice}")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
