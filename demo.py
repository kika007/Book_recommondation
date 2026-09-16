import streamlit as st
import pandas as pd
import pickle

# RECOMMENDATION FUNCTION
def get_recommendations_with_fallback(wanted_isbn, item_sim_df, books_df):

    # plan A or B
    if wanted_isbn in item_sim_df.index:
        st.info("Running similarity calculation...")
        similar_isbns = item_sim_df[wanted_isbn].sort_values(ascending=False)[1:6]
        return similar_isbns.index.tolist()
    else:
        st.warning("The book has too few ratings (searching by author)...")
        book_info = books_df[books_df['ISBN'] == wanted_isbn]

        if book_info.empty:
            return []

        author = book_info.iloc[0]['Book-Author']
        author_books = books_df[books_df['Book-Author'] == author]
        author_books = author_books[author_books['ISBN'] != wanted_isbn]
        return author_books['ISBN'].head(5).tolist()


# LOAD MODEL AND DATA
@st.cache_resource
def load_data():
    try:
        with open('book_recommender_model.pkl', 'rb') as file:
            item_sim_df = pickle.load(file)
    except FileNotFoundError:
        st.error("File book_recommender_model.pkl was not found!")
        item_sim_df = pd.DataFrame()

    try:
        books_df = pd.read_csv('archive/Books.csv')
    except FileNotFoundError:
        st.error("File archive/Books.csv was not found!")
        books_df = pd.DataFrame(columns=['ISBN', 'Book-Title', 'Book-Author'])

    return item_sim_df, books_df

item_sim_df, books_df = load_data()


# UI
st.title("Book Recommendation System")
st.write("Enter part of a book title and the system will find recommendations for you!")

search_query = st.text_input("Enter a word from the title (e.g. Potter, Ring):")

if search_query and not books_df.empty:
    mask = books_df['Book-Title'].str.contains(search_query, case=False, na=False)
    found_books_df = books_df[mask].head(50)

    if found_books_df.empty:
        st.warning("Sorry, we could not find a book with that title. Try another word.")
    else:
        display_to_isbn = {}
        for _, row in found_books_df.iterrows():
            title = row['Book-Title']
            author = row['Book-Author']
            isbn = row['ISBN']
            display_text = f"{title} — {author}"

            if display_text not in display_to_isbn:
                display_to_isbn[display_text] = isbn

        selected_book = st.selectbox("Choose a specific book from the results:", list(display_to_isbn.keys()))

        if st.button("Find me books"):
            wanted_isbn = display_to_isbn.get(selected_book)

            if wanted_isbn:
                recommended_isbns = get_recommendations_with_fallback(wanted_isbn, item_sim_df, books_df)

                if recommended_isbns:
                    st.success("Here are your recommendations:")

                    shown_books = set()
                    counter = 1

                    for isbn in recommended_isbns:
                        result_info = books_df[books_df['ISBN'] == isbn]

                        if not result_info.empty:
                            nice_title = result_info.iloc[0]['Book-Title']
                            author = result_info.iloc[0]['Book-Author']
                            unique_key = f"{nice_title} - {author}"

                            if unique_key not in shown_books:
                                st.write(f"**{counter}. {nice_title}** *(by: {author})*")
                                shown_books.add(unique_key)
                                counter += 1

                            if counter > 5:
                                break

                    if counter == 1:
                        st.warning("We only found other editions of this book, no new recommendations.")
                else:
                    st.warning("We did not find any further recommendations for this book (or author).")