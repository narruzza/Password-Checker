import gooeypie as gp

# Function to load common passwords from a file
def load_common_passwords(filename):
    with open(filename, 'r') as file:
        common_passwords = file.read().splitlines()
    return common_passwords

# Load common passwords
common_passwords = load_common_passwords('Common Credentials 10k.txt')

# Check password strength
def check_password_strength(password):
    strength = 0
    criteria_met = 0

    # Check length
    if len(password) >= 8:
        criteria_met += 1
    if len(password) >= 12:
        criteria_met += 1

    # Check for numbers
    has_number = False
    for char in password:
        if char.isdigit():
            has_number = True
            break
    if has_number:
        criteria_met += 1

    # Check for uppercase
    has_uppercase = False
    for char in password:
        if char.isupper():
            has_uppercase = True
            break
    if has_uppercase:
        criteria_met += 1

    # Check for special characters
    for char in password:
        if not char.isalnum():
            criteria_met += 1
            break

    # Check if password is in the common passwords list
    if password in common_passwords:
        criteria_met = 0  # Set strength to 0 if password is common

    # Calculate strength as a percentage with the criteria met
    strength = (criteria_met / 4) * 100

    return strength

# Function to handle the button click event
def check_strength(event):
    password = password_input.text
    strength = check_password_strength(password)

    # Update the progress bar and strength thingy
    progress_bar.value = strength
    if strength >= 0 and strength < 20:
        strength_label.text = 'Password Strength: Beta ahh password'
    elif strength >= 20 and strength < 40:
        strength_label.text = 'Password Strength: Weak ahh password'
    elif strength >= 40 and strength < 60:
        strength_label.text = 'Password Strength: Mid ahh password'
    elif strength >= 60 and strength < 80:
        strength_label.text = 'Password Strength: Strong ahh password'
    elif strength >= 80 and strength <= 100:
        strength_label.text = 'Password Strength: Sigma ahh password'

# Create the app
app = gp.GooeyPieApp('Password Strength Checker')

# Create widgets
password_label = gp.Label(app, 'Enter your password:')
password_input = gp.Secret(app)
check_button = gp.Button(app, 'Submit Password', check_strength)
progress_bar = gp.Progressbar(app)
strength_label = gp.Label(app, '')

# Add some widgets
app.set_grid(4, 2)
app.add(password_label, 1, 1, align='right')
app.add(password_input, 1, 2)
app.add(check_button, 2, 1, column_span=2)
app.add(progress_bar, 3, 1, column_span=2, fill=True)
app.add(strength_label, 4, 1, column_span=2)

# Run the app
app.run()