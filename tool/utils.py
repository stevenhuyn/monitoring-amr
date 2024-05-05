def process_data(search_results, process_variables = False, variables = None, formatted_variables = None):
    valid_results = []
    for result in search_results:
        if result.contains_AMR:
            valid_results.append(result)

    if process_variables:    
        for result in valid_results:
            processing_text = result.text_response.split('\n')
            for i,variable in enumerate(variables):
                for text in processing_text:
                    if variable +':' in text.lower():
                        result.set_variable(formatted_variables[i],text.split(':')[1].strip())
                        continue
    return valid_results

