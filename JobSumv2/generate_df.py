def generate_dataframe(site_name, search_term, location = None, results_wanted = None, country = None):
    # Your data processing logic goes here
    # For demonstration purposes, let's create a simple DataFrame
    params = {
        'site_name': [site_name],
        'search_term': search_term,
        'location': location,
        'results_wanted': results_wanted,
        'country_indeed': country
    }

    filtered_params = {key: value for key, value in params.items() if value is not ''}
    jobs = scrape_jobs(**filtered_params)
    return jobs