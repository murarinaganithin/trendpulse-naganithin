import pandas as pd
import glob
import os

def main():
    # grab all the json files in the data folder
    json_files = glob.glob("data/trends_*.json")
    
    # just in case task 1 wasn't run yet
    if not json_files:
        print("Couldn't find any JSON files. Run task 1 first.")
        return

    # find the most recently created one
    latest_file = max(json_files, key=os.path.getctime)

    # load the raw data into pandas
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")

    # clean up duplicates using the post id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    # drop any rows that are missing core fields
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # fill empty comments with 0, then force score and comments to be ints
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    df['score'] = df['score'].astype(int)

    # filter out unpopular stories
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # clean up extra spaces at the start/end of titles
    df['title'] = df['title'].str.strip()

    # save the cleaned up dataframe to a csv (dropping the index column)
    csv_filename = "data/trends_clean.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved {len(df)} rows to {csv_filename}")

    # print out how many stories we have left in each category
    print("Stories per category:")
    print(df['category'].value_counts().to_string())

if __name__ == "__main__":
    main()