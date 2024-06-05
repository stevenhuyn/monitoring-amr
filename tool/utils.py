from fuzzywuzzy import fuzz as fz

def compare_phrases(phrase1 ='', phrase2 ='', threshold = 87):
    similarity = fz.ratio(phrase1, phrase2)
    print(similarity)
    return similarity >= threshold

def process_data(search_results,check_text = False, process_variables = False, variables = None, formatted_variables = None):
    valid_results = []
    if check_text:
        for result in search_results:
            if len(result.text) > 100:
                valid_results.append(result)
        return valid_results

    for result in search_results:
        if result.contains_AMR:
            valid_results.append(result)

    if process_variables:    
        for result in valid_results:
            processing_text = result.text_response.split('\n')
            for i,variable in enumerate(variables):
                result.set_variable(formatted_variables[i],'')
                for text in processing_text:
                    if variable.lower() +':' in text.lower() or compare_phrases(variable.lower(),text.lower().split(':')[0]):
                        result.set_variable(formatted_variables[i],text.split(':')[1].strip())
                        continue
    return valid_results

def main():
    print(compare_phrases("pathogen_type","pathogen type"))

if __name__ == "__main__":
    main()
