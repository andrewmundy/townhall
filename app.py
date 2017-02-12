from flask import Flask, render_template, url_for, redirect, request, flash
from collections import namedtuple
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

app = Flask(__name__)

#pubnub setup
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-7d26f194-f129-11e6-acae-0619f8945a4f"
pnconfig.publish_key = "pub-c-3c89c35e-30fc-448f-9978-561ad8285b40"
pnconfig.ssl = True
 
pubnub = PubNub(pnconfig)

#object to store on pubnub
Representative = namedtuple("Representative", "firstname, lastname, city")
Townhall = namedtuple("Townhall", "description, date, representative")
Question = namedtuple("Question", "text, firstname, lastname, address")

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/representative')
def representative():
	if not all(key in request.args for key in ['first', 'last', 'city']):
		return redirect(url_for('index'))
	return render_template('rep.html', first=request.args['first'], last=request.args['last'], city=request.args['city'])


@app.route('/representative/<lastname>/links', methods=['GET', 'POST'])
def links(lastname):
	if request.method == 'POST':
		rep = Representative(request.form['first'], request.form['last'], request.form['city'])
		townhall = Townhall(request.form['desc'], request.form['date'], rep)

		lastname = request.form['last'].lower()
		city = request.form['city'].lower()

		def check(result, status):
			if status.error:
				raise Exception("PubNub Publishing Failed")

		# send lastname to the City:sf channel
		pubnub.publish().channel('City:' + city).message(lastname)\
        .should_store(True).use_post(True).async(check)

		# send str(townhall) to the Name:feinstein channel
		pubnub.publish().channel('Name:' + lastname).message(str(townhall))\
        .should_store(True).use_post(True).async(check)

	return render_template('links.html', last=lastname)

@app.route('/representative/<lastname>', methods=["GET", "POST"])
def dashboard(lastname):
	# get all things pushed to Name:feinstein
	envelope = 	pubnub.history().channel('Name:' + lastname).reverse(True).sync()
	stuff = [line.entry for line in envelope.result.messages]
	# TODO
	questions = []
	townhall = eval(stuff[0])
	for s in stuff[1::]:
		eval(s)
		questions.append([s.text, s.firstname, s.lastname, s.address])
		print(questions)
		
	return render_template('dash.html', envelope=envelope, townhall=townhall, questions=questions)



@app.route('/participant')
def participant():
	if "city" not in request.args:
		return redirect(url_for('index'))
	try:
		city = request.args['city']

		# get the first thing pushed to the City:sf channel (the lastname of the representative)
		envelope = pubnub.history().channel('City:' + city.lower()).reverse(True).count(1).sync()
		messages = envelope.result.messages
		if not messages:
			return "Your rep hasn't set up a townhall in your city. Tell them you are interested in them holding a SpeakNow Townhall!"
		lastname = messages[0].entry
	except Exception as e:
		return "PubNub Error:{}".format(e)
	return redirect(url_for('townhall', lastname=lastname))


@app.route('/<lastname>', methods=['GET', 'POST'])
def townhall(lastname):
	
	if request.method == 'GET':
		# get the 
			envelope = pubnub.history().channel('Name:' + lastname).reverse(True).count(1).sync()
			messages = envelope.result.messages
			if not messages:
				return "Your rep hasn't set up a townhall. Tell them you are interested in them holding a SpeakNow Townhall!"
			townhall = eval(messages[0].entry)
			return render_template('show.html', date=townhall.date, last=lastname, submitted='submitted' in request.args)
	else:
		# create question
		question = Question(request.form['question'], request.form['first'], request.form['last'], request.form['address'])

		print(question)
		
		# TODO
		# take questions and put it on the Name:feinstein channel
			# someone creates comment

		def check(result, status):
			if status.error:
				raise Exception("PubNub Publishing Failed")

		pubnub.publish().channel('Name:' + lastname).message(str(question))\
			.should_store(True).use_post(True).async(check)

		return redirect(url_for('townhall', lastname=lastname, submitted=True))
		

    
if __name__ == "__main__":
	app.run(port=4001, debug=True)














