def get_table_download_link(df):
    # Generates a link allowing the DataFrame to be downloaded as a CSV file.
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="data_extraction.csv">Download CSV File</a>'
    return href