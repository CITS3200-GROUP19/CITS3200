# Import Flask module
# Render template attaches HTML template from templates directory to this app
from flask import Flask, render_template, request
# Import pydicom module to process DICOM files
import pydicom

# DICOM processing
filename = 'example.dcm'
# Reading DICOM file
ds = pydicom.dcmread(filename)
# DICOM data tags
fields = ds.dir()

# Tells where app located
app = Flask(__name__)

#Setup route so dont 404

@app.route('/')
def index():
    return render_template('index.html')

# DICOM field search
@app.route('/', methods=['POST'])
def my_form_post():
        # Retrieves form text
        text = request.form['text']
        # Search DICOM dataset for tag corresponding to form data
        # return ds.dir[text]
        if text in ds:
            return getattr(ds, text)
        return 'No such field exists'


# Run app in debug mode (shows errors)
if __name__ == "__main__":
    app.run(debug=True)
