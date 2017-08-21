from flask import Flask, render_template, request, jsonify, url_for
from parser import Parser

app = Flask(__name__)
p = Parser('stats.json')

@app.route('/', methods=["GET", "POST"])
def stats():

	year = 2016

	if request.method == "POST":
		year = int(request.form['year'])
		ball_striking_data = p.get_ballstriking_data(year)
		scoring_data = p.get_scoring_data(year)
		return render_template('index.html', b = ball_striking_data,
								s = scoring_data, current_year = year)
	else:
		ball_striking_data = p.get_ballstriking_data(year)
		scoring_data = p.get_scoring_data(year)
		return render_template('index.html', b = ball_striking_data, 
							s = scoring_data, current_year = year)

if __name__ == "__main__":
    app.run(debug=True)
