import string

# Function to calculate the entropy of a password
def calculate_entropy(password):
    charset_size = len(set(password))  # Number of unique characters in the password
    password_length = len(password)    # Length of the password
    entropy = password_length * (charset_size).bit_length()  # Calculate entropy
    return entropy

# Function to estimate time to brute-force a password
def estimate_time_to_crack(password, attempts_per_second):
    charset_size = len(set(password))  # Number of unique characters in the password
    password_length = len(password)    # Length of the password
    
    # Calculate the total number of possible combinations
    possible_combinations = charset_size ** password_length
    
    # Estimate the time in seconds
    time_in_seconds = possible_combinations / attempts_per_second
    
    # Convert time in seconds to time in years
    seconds_in_a_year = 60 * 60 * 24 * 365
    time_in_years = time_in_seconds / seconds_in_a_year
    
    return time_in_years

# Function to convert time in years to a readable format
def convert_time_to_readable_format(years):
    if years < 1/365:
        hours = years * 365 * 24
        return f"{hours:.2f} hours"
    elif years < 1:
        days = years * 365
        return f"{days:.2f} days"
    elif years < 1e3:
        return f"{years:.2f} years"
    elif years < 1e6:
        return f"{years/1e3:.2f} thousand years"
    elif years < 1e9:
        return f"{years/1e6:.2f} million years"
    elif years < 1e12:
        return f"{years/1e9:.2f} billion years"
    else:
        return f"{years/1e12:.2f} trillion years"

# Example usage
if __name__ == "__main__":
    # Prompt user to enter a password
    password = input("Enter your password to check its strength: ")
    
    # Number of attempts per second (1 billion guesses per second in this example)
    attempts_per_second = 1e9
    
    # Calculate the entropy of the password
    entropy = calculate_entropy(password)
    
    # Estimate the time to crack the password in years
    time_to_crack_years = estimate_time_to_crack(password, attempts_per_second)
    
    # Convert the time to a more readable format
    readable_time = convert_time_to_readable_format(time_to_crack_years)
    
    # Print the entropy and estimated time to crack the password
    print(f"Password Entropy: {entropy} bits")
    print(f"Estimated Time to Crack: {readable_time}")
