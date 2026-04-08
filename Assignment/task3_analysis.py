import pandas as pd
import numpy as np

def main():
    
    # load the clean data from task 2
    df = pd.read_csv("data/trends_clean.csv")
    
    # print shape and top 5 rows
    print(f"Loaded data: {df.shape}")
    print("First 5 rows:")
    print(df.head())
    
    # quick look at the overall averages
    print(f"Average score   : {df['score'].mean():,.0f}")
    print(f"Average comments: {df['num_comments'].mean():,.0f}")

    print("\n--- NumPy Stats ---")
    
    # grab the score column as a raw numpy array to do math on it
    scores_array = df['score'].to_numpy()
    
    # calculate stats using numpy directly
    mean_score = np.mean(scores_array)
    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {np.median(scores_array):,.0f}")
    print(f"Std deviation: {np.std(scores_array):,.0f}")
    print(f"Max score    : {np.max(scores_array):,.0f}")
    print(f"Min score    : {np.min(scores_array):,.0f}")

    # find which category occurs the most
    cat_counts = df['category'].value_counts()
    print(f"Most stories in: {cat_counts.index[0]} ({cat_counts.iloc[0]} stories)")

    # get the row with the max comments and print its details
    top_idx = df['num_comments'].idxmax()
    top_story = df.loc[top_idx]
    print(f'Most commented story: "{top_story["title"]}" — {top_story["num_comments"]:,} comments')

    
    # calculate engagement ratio (adding 1 so we never divide by zero)
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # boolean column: True if the score is above the numpy mean we calculated earlier
    df['is_popular'] = df['score'] > mean_score

    #Save the Result
    
    # save to a new csv, dropping the index column
    df.to_csv("data/trends_analysed.csv", index=False)
    print("\nSaved to data/trends_analysed.csv")

if __name__ == "__main__":
    main()