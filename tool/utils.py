def process_data(search_results, process_variables = False, variables = None, formatted_variables = None):
    for i, result in enumerate(search_results):
        if not(result.contains_AMR):
            search_results.pop(i)
    
    if process_variables:    
        for result in search_results:
            processing_text = result.text_response.split('\n')
            for i,variable in enumerate(variables):
                for text in processing_text:
                    if variable +':' in text.lower():
                        result.set_variable(formatted_variables[i],text.split(':')[1].strip())
                        continue

