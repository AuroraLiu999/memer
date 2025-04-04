# Import required Flask modules and dependencies
from flask import *
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from helper_functions import login, signup

# Initialize the Flask application
app = Flask(__name__)
UPLOAD_PATH = 'static/uploads'
app.config['UPLOAD_PATH'] = UPLOAD_PATH
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Maximum 5MB
app.secret_key = "123456"

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Check if a filename has an allowed extension.

    Args:
        filename (str): The name of the file to check
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure upload directory exists
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)


@app.route('/', methods=["GET", "POST"]) # Handle both GET and POST requests to /mainpage
def index():
    """
    Render the mainpage of the web application.
    
    Returns:
        Rendered template: The main HTML page for the application (mainpage.html)
    """
    return render_template('mainpage.html')

@app.route('/login', methods=["GET", "POST"]) # Handle both GET and POST requests to /login
def login_page():
    """
    Handle user login.
    
    Processes login form submissions (POST) and displays loginpage (GET).

    Stores username in session and redirects to index page for successful login
    
    Shows error message and redisplays login page for failure login
    
    Returns:
        Response: Either a redirect or rendered login template
    """

    # Extract from form submission
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Simplified login validation (use proper authentication in production)
        # if username and password:
        #    session["username"] = username
        #    return redirect(url_for('index'))
        user_id = login(username, password)
        print(f"User id : {user_id}")
        if user_id:
            print("Main if ")
            # Successful login
            session["username"] = username
            return redirect(url_for('index'))
        else:
            # Failed login
            flash("Incorrect username or password", "error")

     # For GET requests or failed POST attempts, show login page
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"]) # Handle both GET and POST requests to /signup
def signup_page():
    """
    Handle user registration.
    
    Processe signup form submissions (POST) and display signup page (GET).
    Validate password confirmation match before registration.
    
    Returns:
        Response: Either a redirect to index (success) or rendered signup template (failure/GET)
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]

        # Validate password confirmation
        if confirmpassword != password:
            flash("Passwords do not match", "error")
            return render_template("signup.html")
        
        # Use helper function to register user
        user_id = signup(username, password)
        
        if user_id:
            # Successful registration
            session["username"] = username
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login_page'))
        else:
            # Username already exists
            flash("Username already exists", "error")
            return render_template("signup.html")
    
    # Display empty signup form for GET requests
    return render_template("signup.html")

    # # Extract form data
    # if request.method == "POST":
    #     username = request.form["username"]
    #     password = request.form["password"]
    #     confirmpassword = request.form["confirmpassword"]

    #     # Validate password confirmation
    #     if confirmpassword != password:

    #         # Error feedback
    #         flash("Passwords do not match", "error")

    #          # Redisplay form with error
    #         return render_template("signup.html")
        
    #     # Simplified registration (encrypt passwords in production)
    #     session["username"] = username

    #     # Redirect to homepage
    #     return redirect(url_for('index'))
    
    # # Display empty signup form for GET requests
    # return render_template("signup.html")

@app.route('/upload', methods=['GET','POST']) # Handle both GET and POST requests to /upload
def upload_file():
    """
    Handle file upload for users.
    
    GET: Displays the upload form
    POST: Processes file upload with validation
    
    Returns:
        Response: Redirects or renders template based on operation success/failure
    """

    # Authentication check
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':

        # Validate file presence in request
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']

        # Check for empty filename
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Validate file type
        if file and allowed_file(file.filename):
            try:

                # Generate unique filename with username and timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{session['username']}_{timestamp}_{secure_filename(file.filename)}"
                
                # Save file
                filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
                file.save(filepath)
                
                flash('File uploaded successfully!', 'success')
                return redirect(url_for('mymeme_page'))
            except Exception as e:

                # Handle filesystem errors
                flash(f'Upload error: {str(e)}', 'error')
                return redirect(request.url)
            
        else:
            # Invalid file type feedback
            flash('Allowed file types: png, jpg, jpeg, gif', 'error')
            return redirect(request.url)
        
    # Display upload form for GET requests
    return render_template("upload.html", username=session["username"])

# Define a route for '/user_profile' that accepts both GET and POST requests
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    # Check if user is not logged in (username not in session)
    if 'username' not in session:
        # Redirect to login page if user is not authenticated
        return redirect(url_for('login_page'))
    # Render the user profile page (mypage.html) with the username from session
    return render_template('mypage.html', username=session['username'])


@app.route('/mymeme', methods=['GET'])
def mymeme_page():
    """
    Handle the '/mymeme' route to display user-specific memes.
    This page shows all memes uploaded by the currently logged-in user.
    """

    # Redirect to login page if user is not logged in
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    # Initialize list to store image information
    image_files = []

    # Scan the upload directory for files belonging to the current user
    for filename in os.listdir(app.config['UPLOAD_PATH']):

        # Check if file belongs to current user
        if filename.startswith(session['username'] + '_'):
            filepath = os.path.join(app.config['UPLOAD_PATH'], filename)

            # Ensure it's a file
            if os.path.isfile(filepath):

                # Get file information
                stat = os.stat(filepath)
                upload_time = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                
                # Extract display name by removing username and timestamp from filename
                display_name = '_'.join(filename.split('_')[2:])  # Remove username and timestamp
                
                # Add file information to the list
                image_files.append({
                    'name': display_name,
                    'path': filename,
                    'upload_time': upload_time
                })

    # Render the template with user's meme information
    return render_template('mymeme.html', 
                         username=session['username'], 
                         images=image_files)



@app.route('/monkey', methods=['GET'])
def monkey(): 
    """
    Monkey template routes
    """ 
    return render_template("monkey.html")


@app.route('/chinese', methods=['GET'])
def chinese(): 
    """
    Chinese template routes
    """
    return render_template("chinese.html")


@app.route('/panda', methods=['GET'])
def panda(): 
    """
    Panda template routes
    """ 
    return render_template("panda.html")


@app.route('/emotion', methods=['GET'])
def emotion(): 
    """
    Emotion template routes
    """ 
    return render_template("emotion.html")


@app.route('/chat', methods=['GET'])
def chat(): 
    """
    Chat template routes
    """ 
    return render_template("chat.html")


@app.route('/cat', methods=['GET'])
def cat(): 
    """
    Cat template routes
    """ 
    return render_template("cat.html")


@app.route('/bear', methods=['GET'])
def bear(): 
    """
    Bear template routes
    """ 
    return render_template("bear.html")


@app.route('/dog', methods=['GET'])
def dog(): 
    """
    Dog template routes
    """ 
    return render_template("dog.html")


@app.route('/trump', methods=['GET'])
def trump(): 
    """
    Trump template routes
    """ 
    return render_template("trump.html")


@app.route('/logout')
def logout():
    """
    Handle user logout.
    Clears the user's session and redirects to the index page.
    """ 

    # Remove the 'username' from the session if it exists
    session.pop('username', None)

    # Redirect to the user's index page after logout
    return redirect(url_for('index'))



if __name__ == '__main__':
    """
    Main entry point for running the Flask application.
    This block ensures the server only starts when the script is executed directly,
    not when imported as a module.
    """ 
    app.run(debug=True)