import os
from statistics import mode
import settings
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
)
from middleware import model_predict

router = Blueprint("app_router", __name__, template_folder="templates")





# def index():
#     """
#     GET: Index endpoint, renders our HTML code.

#     POST: Used in our frontend so we can upload and show an image.
#     When it receives an image from the UI, it also calls our ML model to
#     get and display the predictions.
#     """

#     if request.method == "GET":
#         return render_template("index.html")

#     if request.method == "POST":
#             report = request.form.get("numberpoints")
#             clf = load('pipe.joblib')
#             answer = clf.predict(np.array(report).reshape(-1, 1))
#             flash(f"Your score:{report}, Your predicted salary:{answer}")
#             return redirect(request.url)
#             #return render_template("index.html")

#     return render_template("index.html")



@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    if request.method == "GET":
        return render_template("index.html")
    # Store the reported data to settings.FEEDBACK_FILEPATH
    if request.method =='POST':
      report = request.form.get("numberpoints")
      print(report)
      flash(report)
      prediction = model_predict(report)
      flash(prediction)
      return render_template("index.html")

        # # No form received, show basic UI
        # if "form" not in request.form:
        #     flash("No form submited")
        #     return redirect(request.url)

        # # File received but no filename is provided, show basic UI
        # form = request.form["form"]
        # if form == "":
        #     flash("No information provided")
        #     return redirect(request.url)

        # # File received and it's an image, we must show it and get predictions
        # try:
        #   pts = float(form)
        # except: 
        #   flash("You must submit a float!")
        #   return redirect(request.url)
        
        # if form and (type(pts) == float):            
        #     prediction = model_predict(pts)
            
        #     return render_template("index.html", prediction=prediction)
          
        # # File received and but it isn't an image
        # else:
        #     flash("You must submit a float!")