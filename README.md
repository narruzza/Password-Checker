# Password Strength Checker
<img src="https://github.com/narruzza/Password-Checker/blob/master/DALL%C2%B7E%20June%203%20Logo%20for%20PassGuard.jpg" alt="alt text" width="400" height="400">

Welcome to the **Password Strength Checker** app! This tool is designed to help users evaluate the strength of their passwords to ensure they are strong and secure.

## Overview
The Password Strength Checker checks passwords against several criteria including length, character variety, and common passwords. It also provides visual feedback on the password strength.

## Features
- **Password Length Check**: Ensures passwords meet minimum length requirements.
- **Character Variety Check**: Verifies the inclusion of numbers, uppercase letters, and special characters.
- **Common Passwords Check**: Compares against a list of 10,000 common passwords to avoid easy-to-guess passwords.
- **Visual Feedback**: Provides a progress bar and descriptive labels to indicate password strength.
- **HIBP Integration**: Checks if the password has been compromised in any known data breaches.
<img src="https://github.com/narruzza/Password-Checker/blob/master/June%2018%20Screen%20Recording.gif" alt="alt text" width="600" height="400">

## Installation
To run the Password Strength Checker, you'll need Python installed on your machine along with the GooeyPie library.

1. Clone the repository:
git clone https://github.com/yourusername/password-strength-checker.git
2. Navigate to the project directory:
cd password-strength-checker
3. Install the required libraries:
pip install gooeypie pyhibp pyperclip zxcvbn
4. Run the application:
python main.py

## Usage
Enter your desired password in the input field.
Click the "Submit Password" button.
View the strength of your password via the progress bar and strength label.

## Contributing
We welcome contributions to improve the Password Strength Checker! Feel free to submit issues and pull requests.

## License
This project is licensed under the MIT License.

## Troubleshooting
If the HIBP check does not work on your network, the application will notify you with a message.

## Contact
For any questions or suggestions, please feel free to open an issue on GitHub.
