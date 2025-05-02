import streamlit as st
import pandas as pd #This imports Pandas, a powerful library for working with data (like tables, spreadsheets, CSV files).
import os #These are tools to handle input/output, especially for handling file uploads/downloads in memory (without saving them on disk).
from io import BytesIO #work with binary files like csv or excel

st.set_page_config(page_title= "🧹Data sweeper", layout= "wide")

#custom css
st.markdown(


"""
<style>
.stApp{
    background-color : black;
    color: white;


}
</style>
""",
   unsafe_allow_html=True
)

#title and description
st.title("🧹DATA SWEEPER")
st.write("📂Transform your files between Csv and excel format with Built-in Data_cleaning and visualization")

#file upload
Uploaded_files = st.file_uploader("upload your file(accept only Csv and excel)", type=["CSV","xlsx"] , accept_multiple_files=True)


if Uploaded_files:
    for file in Uploaded_files:
     file_ext = os.path.splitext(file.name)[-1].lower() #This splits the file name into two parts: the name and the extension (like .pdf, .jpg, etc.).

     if file_ext == ".csv":
        df = pd.read_csv(file) #pandas are used to read file and store it content in Dataframe called df
     elif file_ext == ".xlsx":
        df = pd.read_excel(file)
     else:
        st.error(f"unsupported file type: {file_ext}")
        continue   #when error occur the continue will jump to the next loop

     #file detail
     st.write(" Preview the head of the DataFrame")
     st.dataframe(df.head())  #df.head() is a pandas function that shows the first 5 rows of a DataFrame (df). df is a table 
       
     #Data cleaning options
     st.subheader("Data cleaning options")
     if st.checkbox(f"Clean data for {file_ext}"):
        col1 , col2 = st.columns(2)  

        with col1:
           if st.button(f"Remove duplicate from the files: {file.name}"): #When the user clicks the button, the code inside this if block will run.
              
              df.drop_duplicates(inplace=True) #This removes duplicate rows from the data table (df). If two or more rows have the exact same values, only one is kept and INPLACE=TRUE means the original files will directly update
              
              st.write("Duplicate removed")


        with col2:
           if st.button(f"✅ Fill the missing value for: {file.name}"):
              numeric_col = df.select_dtypes(include=['number']).columns #This line selects all numeric columns (e.g., integers and floats) in the DataFrame. It stores the column names in numeric_col
              df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
              st.write("✅ Missing value have been filled")



           #Selection columns
        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns for: {file.name}", df.columns, default=df.columns)
        df = df[columns] #This updates the DataFrame to keep only the columns the user selected.

           #Data visualization
        st.subheader("Data visualization")
        if st.checkbox(f"Showing visualization for {file.name}"):# if checkbox is clicked the barchart will be shown
              st.bar_chart(df.select_dtypes(include='number').iloc[:, :2]) #df.select_dtypes(include='number' this will only select numerical columns of file #iloc only first two columns of data frame

         # Data conversion  
        st.subheader("Data visualization")
        conversion_type = st.radio(f"Convert {file.name} to:", ["Csv" , "Excel" ], key=file.name)
        if st.button(f"convert {file.name}"):
           buffer = BytesIO() #byteio is an temporary memory file which is built in RAM
           if conversion_type == "Csv":
               df.to_csv(buffer , index=False)
               file_name = file.name.replace(file_ext, ".csv")
               mime_type = "text/csv"

           elif conversion_type == "Excel":
               df.to_excel(buffer , index=False)
               file_name = file.name.replace(file_ext, ".xlsx")
               mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
           buffer.seek(0)

           st.download_button(
               label = f"Download {file_name} as {conversion_type}",
               data = buffer,
               file_name=file_name,
               mime = mime_type
              )  
st.success("✅All file processed successfully")



                
