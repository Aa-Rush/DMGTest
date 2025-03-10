import sys
import requests

def api_call(curr_code,url="https://v6.exchangerate-api.com/v6/f16d88a620a2c299b09b7a91/latest/"):
    #Sets up API call to free currency exhange rate API. My private code is currently hardcoded in the URL, but easy to change.
    #Would normally pull an encoded key and decode and f string into the URL.
    #Free API in use sends all currency conversion rates, there are better paid API's that can do the conversion as part of call.
    #Curr_code is the currency we are converting to.
    response = requests.get(url+curr_code)
    if response.status_code != 200:
        data = response.json()
        #Using the API's error handling to return a more informative error message
        print(f"Error in API Call: {data['error-type']}")
        sys.exit(1)
    return response

def calc_conversion(to_curr, from_curr, amount):
    #Calculates the conversion rate from the API call and the amount to convert.
    #Run API call to get conversion rate
    response = api_call(from_curr)
    #Parse reponse json
    data = response.json()
    #Isolate the return we care about
    conversion_rate = data['conversion_rates']
    #Iterate over returned list of rates and find the one we want.
    for curr in conversion_rate:
        if curr == to_curr:
            conversion_rate = conversion_rate[curr]
            break
    if conversion_rate == 0 or conversion_rate == None:
        #The API in use shouldn't return 0 or None based on documentation, but better safe than sorry.
        print("Error: No conversion rate found for the given currency")
        sys.exit(1)
    #Convert
    new_total = amount * conversion_rate
    return new_total, conversion_rate

def curr_code_valditaton(curr_code):
        if not isinstance(curr_code, str) or curr_code.isalpha() == False or len(curr_code) != 3:
            print("Error: Currency code does not look valid. Please use a 3 letter currency code.")
            sys.exit(1)

def convert(amount: float, to_curr: str, from_curr: str):
    #Main function that calls the conversion function and prints the results.
    new_total, conversion_rate = calc_conversion(to_curr, from_curr, amount)
    #Return result, rounded to 2 decimal places including trailing 0
    print(f"{round(amount,2):.2f} {from_curr} is equal to {round(new_total, 2):.2f} {to_curr} at a conversion rate of {conversion_rate}")

#Run the script when called
if __name__ == "__main__":
    from_curr=input("Enter the currency code you are converting from. e.g. USD: ")
    #Validate
    curr_code_valditaton(from_curr)
    
    amount=input("Enter the amount you want to convert: ")
    #Validate. Did not create seperate function as only used once.
    try:
        float(amount)
    except ValueError:
        print("Error: Amount must be a number")
        sys.exit(1)
    if float(amount) < 0:
        print("Error: Amount must be a positive number")
        sys.exit(1)


    to_curr=input("Enter the currency you are converting to. e.g. GBP: ")
    #Validate
    curr_code_valditaton(to_curr)
    
    convert(float(amount), to_curr.upper(), from_curr.upper())
    
#There are improvements that could be made. 
# First, I would prefer to check currency codes against a list of valid codes as part of the input process. This could be done by pulling a list from the API
#first and checking against that. But given there is a rate limit for the free API I am using, I didn't want to make a second call.
# Second, using a more robust API could be beneficial as it could handle the conversion as part of the call, rather than needing to be done manually.
# Lastly, I would prefer for error handling to be more descriptive. As stated above, I utilize the API error codes as in my experience they are more informative
#but in the case of the one is use it is hit or miss on the quality of the error message.
# As this is a simple tool to run conversions, I decided to go with a CLI script. If we had a currated list of valid currency codes,
# a GUI might have been more beneficial as we could use a drop down to ensure proper input.