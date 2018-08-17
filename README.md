# medicare_data_analysis
Uses pandas to analyze the public Medicare data on nursing homes and their deficiencies.

'getting_json.py' uses Medicare's API to retrieve the data and then cleans the data for use in 'data_manipulation.py'
Within 'data_manipulation.py' there are multiple distinct functions that are all callable from within the basic UI. The functions available allow the user to perform the following:
 - PRODUCE A DataFrame WITH THE TOTAL NUMBER OF DEFICIENCIES FOR EACH PROVIDER
 - PRODUCE A DataFrame WITH THE TOTAL NUMBER OF OCCURRENCES OF EACH SEVERITY LEVEL
 - PRODUCE A DataFrame WITH THE TOTAL NUMBER OF EACH SEVERITY LEVEL BY PROVIDER
 - PRODUCE A DataFrame WITH THE TOTAL NUMBER OF EACH F TAG ALONG WITH THEIR TYPES AND DESCRIPTIONS
 - PRODUCE A DataFrame WITH THE TOTAL NUMBER OF EACH F TAG BY PROVIDER
 - CHART THE NUMBER OF DEFICIENCIES OVER TIME
 - CHART THE NUMBER OF DEFICIENCIES A ORGANIZATION OR INDIVIDUAL IS RESPONSIBLE FOR OVER TIME
 - RETURN EVERY PROVIDER ASSOCIATED WITH A GROUP OF OWNERS, GIVEN AN ORIGINAL PROVIDER
 
