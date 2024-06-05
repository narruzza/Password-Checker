import requests
import gooeypie as gp
from pyhibp import pwnedpasswords
from pyhibp import set_user_agent
import pyperclip
import zxcvbn

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
password_strength = 0
password_suggestions = []
suggestions_window = None
info_window = None

# Check password strength
def check_password_strength(password):
    global password_suggestions
    criteria_met = 0
    suggestions = set()

    # Check length
    if len(password) >= 8:
        criteria_met += 1
    else:
        suggestions.add("Increase length to at least 8 characters.")
    if len(password) >= 12:
        criteria_met += 1
    else:
        suggestions.add("Increase length to at least 12 characters.")
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
    else:
        suggestions.add("Include at least one number.")

    # Check for uppercase
    has_uppercase = False
    for char in password:
        if char.isupper():
            has_uppercase = True
            break
    if has_uppercase:
        criteria_met += 1
    else:
        suggestions.add("Include at least one uppercase letter.")

    # Check for special characters
    for char in password:
        if not char.isalnum():
            criteria_met += 1
        else:
            suggestions.add("Include at least one special character.")

    # Check if password is in the common passwords list
    if password in common_passwords:
        criteria_met = 0  # Set strength to 0 if password is common
        suggestions.add("Avoid using common passwords.")

    # Calculate strength as a percentage with the criteria met
    if criteria_met < 0:
        criteria_met = 0
    strength = (criteria_met / 5) * 100
    password_suggestions = list(suggestions)

    return strength

# Function to handle the button click event
def check_strength(event):
    password = password_input.text
    strength = check_password_strength(password)
    pwned_count = 0
    
    # Check if the password has been pwned
    try:
        response = requests.get("https://haveibeenpwned.com/api/v3/breaches")
        response.raise_for_status()
        pwned_count = pwnedpasswords.is_password_breached(password)
    except requests.exceptions.RequestException as e:
        pwned_count = None
        pwned_label.text = 'HIBP check not working on current connection'
        print(f'RequestException: {e}')
    except Exception as e:
        pwned_count = None
        pwned_label.text = f'Error checking password: {e}'
        print(f'Exception: {e}')

    # Update the progress bar and strength thingy
    progress_bar.value = strength
    if strength >= 0 and strength < 20:
        strength_label.color = colors[0]
        strength_label.text = 'Password Strength: Beta'
    elif strength >= 20 and strength < 40:
        strength_label.color = colors[1]
        strength_label.text = 'Password Strength: Weak'
    elif strength >= 40 and strength < 60:
        strength_label.color = colors[2]
        strength_label.text = 'Password Strength: Mid'
    elif strength >= 60 and strength < 80:
        strength_label.color = colors[3]
        strength_label.text = 'Password Strength: Strong'
    elif strength >= 80 and strength <= 100:
        strength_label.color = colors[4]
        strength_label.text = 'Password Strength: Sigma'
    
    # Update the pwned label
    if pwned_count > 0:
        pwned_label.color = colors[0]
        pwned_label.text = f'Your cooked. Seen {pwned_count} times in data breaches'
    else:
        pwned_label.color = colors[3]
        pwned_label.text = 'Not pwned! :)'
    
    # Use zxcvbn to estimate crack time
    zxcvbn_result = zxcvbn.zxcvbn(password)
    crack_time_label.text = f"Estimated crack time: {zxcvbn_result['crack_times_display']['offline_slow_hashing_1e4_per_second']}"

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

# Suggestions window
def show_suggestions(event):
    suggestions_window = gp.GooeyPieApp('Password Suggestions')
    suggestions_window.set_grid(2, 1)
    suggestions_label = gp.StyleLabel(suggestions_window, '\n'.join(password_suggestions))
    suggestions_label.font_name = ('Bradley Hand')
    suggestions_title = gp.StyleLabel(suggestions_window, 'Try imporving your password with these suggestions:')
    suggestions_title.font_name = ('Bradley Hand')
    suggestions_window.add(suggestions_label, 2, 1)
    suggestions_window.add(suggestions_title, 1, 1)
    suggestions_window._root.iconphoto = lambda *args: None  # Disable iconphoto
    suggestions_window.run()

def show_info(event):
    global info_window
    info_window = gp.GooeyPieApp('Password Strength Information')
    info_window.set_grid(1, 1)
    info_text = ("Password strength is determined based on the following criteria:\n"
                 "1. Length: At least 8 characters for a minimum strength.\n"
                 "2. Length: At least 12 characters for additional strength.\n"
                 "3. Inclusion of numbers: At least one numerical digit.\n"
                 "4. Inclusion of uppercase letters: At least one uppercase letter.\n"
                 "5. Inclusion of special characters: At least one special character (e.g., @, #, $).\n"
                 "6. Common passwords: Password should not be in the list of common passwords.\n"
                 "Each criterion met adds to the overall strength of the password, calculated as a percentage.")
    info_label = gp.StyleLabel(info_window, info_text)
    info_label.font_name = ('Bradley Hand')
    info_window.add(info_label, 1, 1)
    info_window._root.iconphoto = lambda *args: None  # Disable iconphoto
    info_window.run()

# Create the app
app = gp.GooeyPieApp('PassGuard')

# Create widgets
password_label = gp.StyleLabel(app, 'Enter your password:')
password_label.font_name = ('Bradley Hand')

password_style_label = gp.StyleLabel(app,"Nick")
password_style_label.font_name = ('Bradley Hand')

password_input = gp.Secret(app)

toggle_button = gp.Button(app, 'Show', toggle_password_visibility)

suggestions_button = gp.Button(app, 'Show Suggestions', show_suggestions)

info_button = gp.Button(app, 'Info', show_info)

check_button = gp.Button(app, 'Submit Password', check_strength)

copy_button = gp.Button(app, 'Copy Password', copy_password)

progress_bar = gp.Progressbar(app)

strength_label = gp.StyleLabel(app, '')
strength_label.font_name = ('Bradley Hand')

pwned_label = gp.StyleLabel(app, '')
pwned_label.font_name = ('Bradley Hand')

crack_time_label = gp.StyleLabel(app, '')
crack_time_label.font_name = ('Bradley Hand')

# Add the widgets
app.set_grid(8, 3)
app.set_column_weights(1, 1, 1)
app.add(password_label, 1, 2, align='center')
app.add(password_input, 2, 2, align='center')
app.add(toggle_button, 3, 1, align='center')
app.add(check_button, 3, 2, align='center')
app.add(copy_button, 3, 3, align='center')
app.add(strength_label, 4, 2, align='center')
app.add(progress_bar, 5, 1, column_span=3, fill=True)
app.add(pwned_label, 6, 1, column_span=3, align='center')
app.add(crack_time_label, 7, 1, column_span=3, align='center')
app.add(suggestions_button, 8, 1, align='left')
app.add(info_button, 8, 3, align='right')

# Run the app
app.run()