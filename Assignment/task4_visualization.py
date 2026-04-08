import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # make sure our output folder exists so we don't get an error saving
    os.makedirs("outputs", exist_ok=True)

    # load the analyzed data from task 3
    df = pd.read_csv("data/trends_analysed.csv")


    # Chart 1 - Top 10 Stories 
    # sort by score to get the highest ones at the top, then grab the top 10
    top_10 = df.sort_values(by='score', ascending=False).head(10)
    
    # helper to shorten titles so they fit on the screen. cuts off at 47 chars and adds "..."
    short_titles = top_10['title'].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)

    plt.figure(figsize=(10, 6))
    plt.barh(short_titles, top_10['score'], color='skyblue')
    plt.gca().invert_yaxis() # flip it so the #1 score is at the top of the chart
    
    plt.title("Top 10 Stories by Score")
    plt.xlabel("Score (Upvotes)")
    plt.ylabel("Story Title")
    
    # always save before show!
    plt.tight_layout() # keeps the long labels from getting cut off
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close() # clear the canvas for the next chart


    # Chart 2 - Stories per Category
    category_counts = df['category'].value_counts()
    
    plt.figure(figsize=(8, 6))
    # assign some basic colors to the bars
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    
    plt.bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
    
    plt.title("Number of Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    
    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png")
    plt.close()


    # Chart 3 - Score vs Comments Scatter
    plt.figure(figsize=(8, 6))
    
    # split data into popular and regular so we can easily give them different colors/labels
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]

    # plot both sets of dots on the same chart
    plt.scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', alpha=0.7)
    plt.scatter(not_popular['score'], not_popular['num_comments'], color='grey', label='Regular', alpha=0.5)
    
    plt.title("Story Score vs Number of Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("outputs/chart3_scatter.png")
    plt.close()


    #Bonus - Dashboard 
    # create a 2x2 grid for our 3 charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight='bold')

    # Chart 1 in top-left (axes[0, 0])
    axes[0, 0].barh(short_titles, top_10['score'], color='skyblue')
    axes[0, 0].invert_yaxis()
    axes[0, 0].set_title("Top 10 Stories")

    # Chart 2 in top-right (axes[0, 1])
    axes[0, 1].bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
    axes[0, 1].set_title("Stories per Category")
    axes[0, 1].tick_params(axis='x', rotation=45) # rotate labels so they don't overlap

    # Chart 3 in bottom-left (axes[1, 0])
    axes[1, 0].scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', alpha=0.7)
    axes[1, 0].scatter(not_popular['score'], not_popular['num_comments'], color='grey', label='Regular', alpha=0.5)
    axes[1, 0].set_title("Score vs Comments")
    axes[1, 0].legend()

    # Hide the empty bottom-right chart (axes[1, 1])
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig("outputs/dashboard.png")
    plt.close()
    
    print("All charts successfully generated and saved to the outputs/ folder!")

if __name__ == "__main__":
    main()