def write_api_key_to_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('API_KEY'):
                    print("API key already exists in the file.")
                    return
    except FileNotFoundError:
        pass

    api_key = input("Please enter your API key: ")
    with open(file_path, 'a') as file:
        file.write(f'\nAPI_KEY = "{api_key}"')

write_api_key_to_file('.streamlit/secrets.toml')
