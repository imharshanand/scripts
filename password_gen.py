import random
import string

# Function to generate a password
def generate_password(length=12):
    # Define character sets for different types of characters
    lowercase = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    uppercase = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = string.digits              # '0123456789'
    special = string.punctuation        # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    # Exclude ambiguous characters to avoid confusion
    ambiguous = {'l', '1', 'I', 'O', '0'}
    lowercase = ''.join([char for char in lowercase if char not in ambiguous])
    uppercase = ''.join([char for char in uppercase if char not in ambiguous])
    digits = ''.join([char for char in digits if char not in ambiguous])
    special = ''.join([char for char in special if char not in ambiguous])

    # Combine all character sets into one string
    all_characters = lowercase + uppercase + digits + special

    # Ensure the password contains at least one character from each set
    password = [
        random.choice(lowercase),  # Add a random lowercase letter
        random.choice(uppercase),  # Add a random uppercase letter
        random.choice(digits),     # Add a random digit
        random.choice(special)     # Add a random special character
    ]

    # If the desired length is more than 4, fill the rest with random characters
    if length > 4:
        password.extend(random.choice(all_characters) for _ in range(length - 4))

    # Shuffle the list of characters to ensure randomness
    random.shuffle(password)

    # Join the list of characters into a single string to form the final password
    return ''.join(password)

# Function to calculate the entropy of a password
def calculate_entropy(password):
    # Entropy is a measure of the unpredictability or randomness of a password
    # Higher entropy means higher security
    charset_size = len(set(password))  # Number of unique characters in the password
    password_length = len(password)    # Length of the password

    # Entropy formula: entropy = password_length * log2(charset_size)
    # where charset_size is the number of unique characters used in the password
    entropy = password_length * (charset_size).bit_length()

    # Explanation of (charset_size).bit_length():
    # .bit_length() gives the number of bits required to represent charset_size in binary
    # For example, if charset_size is 64, .bit_length() is 6 because 64 in binary is 1000000 (6 bits)
    # This effectively calculates log2(charset_size) without using floating-point operations
    return entropy

# Example usage
if __name__ == "__main__":
    while True:
        try:
            # Ask the user to input the desired password length
            password_length = int(input("Enter desired password length (minimum 14): "))
            if password_length < 14:
                # Ensure the password length is at least 14
                print("Password length should be at least 14. Please try again.")
                continue
            break
        except ValueError:
            # Handle invalid input that cannot be converted to an integer
            print("Invalid input. Please enter a valid number.")
    
    # Generate the password using the specified length
    password = generate_password(password_length)
    # Calculate the entropy of the generated password
    entropy = calculate_entropy(password)

    # Print the generated password and its entropy
    print(f"Generated Password: {password}")
    print(f"Password Entropy: {entropy} bits")
