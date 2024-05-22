import gooeypie as gp
from pyhibp import pwnedpasswords
from pyhibp import set_user_agent
import pyperclip

colors = ['Red', 'Orange', 'Yellow', 'LimeGreen', 'Green']

# Function to load common passwords from a file
def load_common_passwords(filename):
    with open(filename, 'r') as file:
        common_passwords = file.read().splitlines()
    return common_passwords

# Load common passwords
common_passwords = load_common_passwords('passwords.txt')

# Set the user agent for the pyhibp API
set_user_agent(ua="PassGuard")

password_visible = False

# Check password strength
def check_password_strength(password):
    criteria_met = 0

    # Check length
    if len(password) >= 8:
        criteria_met += 1
    if len(password) >= 12:
        criteria_met += 1
    if len(password) <= 6:
        criteria_met -= 2
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
    if criteria_met < 0:
        criteria_met = 0
    strength = (criteria_met / 5) * 100

    return strength

# Function to handle the button click event
def check_strength(event):
    password = password_input.text
    strength = check_password_strength(password)

    # Check if the password has been pwned
    try:
        pwned_count = pwnedpasswords.is_password_breached(password)
    except Exception as e:
        pwned_count = 0
        pwned_label.text = f'Error checking password: {e}'

    # Update the progress bar and strength thingy
    progress_bar.value = strength
    if strength >= 0 and strength < 20:
        strength_label.color = colors[0]
        strength_label.text = 'Password Strength: Beta ahh password'
    elif strength >= 20 and strength < 40:
        strength_label.color = colors[1]
        strength_label.text = 'Password Strength: Weak ahh password'
    elif strength >= 40 and strength < 60:
        strength_label.color = colors[2]
        strength_label.text = 'Password Strength: Mid ahh password'
    elif strength >= 60 and strength < 80:
        strength_label.color = colors[3]
        strength_label.text = 'Password Strength: Strong ahh password'
    elif strength >= 80 and strength <= 100:
        strength_label.color = colors[4]
        strength_label.text = 'Password Strength: Sigma ahh password'
    
    # Update the pwned label
    if pwned_count > 0:
        pwned_label.color = colors[0]
        pwned_label.text = f'Your fucked. Seen {pwned_count} times in data breaches'
    else:
        pwned_label.color = colors[3]
        pwned_label.text = 'Not pwned! :)'

def toggle_password_visibility(event):
    global password_visible
    password_input.toggle()
    password_visible = not password_visible
    toggle_button.text = 'Hide' if password_visible else 'Show'

# Copy password
def copy_password(event):
    pyperclip.copy(password_input.text)
    copy_button.text = 'Copied!'
    app.after(2000, reset_copy_button)  # Reset the button text after 2 seconds

# Reset copy button text
def reset_copy_button():
    copy_button.text = 'Copy'

# Create the app
app = gp.GooeyPieApp('PassGuard')

# Create widgets
password_label = gp.Label(app, 'Enter your password:')
password_label.font = ('Arial', 12, 'bold')

password_style_label = gp.StyleLabel(app,"Nick")

password_input = gp.Secret(app)

toggle_button = gp.Button(app, 'Show', toggle_password_visibility)
toggle_button.font = ('Arial', 12)  # Adjust font size here

check_button = gp.Button(app, 'Submit Password', check_strength)

copy_button = gp.Button(app, 'Copy Password', copy_password)

progress_bar = gp.Progressbar(app)

strength_label = gp.StyleLabel(app, '')
strength_label.font = ('Arial', 12)

pwned_label = gp.StyleLabel(app, '')
pwned_label.font = ('Arial', 12)

# Add the widgets
app.set_grid(8, 3)
app.set_column_weights(1, 2, 1)
app.add(password_label, 1, 1, align='right')
app.add(password_input, 1, 2, align='left')
app.add(toggle_button, 1, 3, align='left')
app.add(check_button, 2, 1, column_span=3, align='center')
app.add(copy_button, 3, 1, column_span=3, align='center')
app.add(progress_bar, 4, 1, column_span=3, fill=True)
app.add(strength_label, 5, 1, column_span=3, align='center')
app.add(pwned_label, 6, 1, column_span=3, align='center')

# Run the app
app.run()