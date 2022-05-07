
from flask import Flask, redirect, render_template, request, jsonify,json, flash, session
import requests
from API_key import app_id, api_key, next_trips_url
from forms import AddLateBusForm, Login, SignUp, GetData
from models import db, connect_db, User, Submitted_Data
from datetime import datetime
from functions import get_username, calculate_time, Validator, get_busNo_from_gtfs_routes_text, get_stopNo_from_gtfs_stops_text, get_search_query_data,extract_search_query_data


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)



@app.route('/')
def home_page():
    u = get_username()
    form = GetData()
    datapoints = len(Submitted_Data.query.all())
    no_shows_amount = len(Submitted_Data.query.filter_by(noShow=True).all())
    delays_arr = Submitted_Data.query.filter_by(noShow=False).all()
    total_delay_time = calculate_time(delays_arr)

    
    
    return render_template('home.html', u=u, datapoints=datapoints, no_shows_amount=no_shows_amount,total_delay_time=total_delay_time, form = form)


@app.route('/next_bus', methods=['GET'])
def next_bus():
    u = get_username()
    return render_template('next_bus.html', u=u)


@app.route('/next_bus_times', methods=['GET'])
def next_bus_times():
    stopNo = request.args['stopNo']
    busNo = request.args['busNo']
    
    res = requests.get(f'{next_trips_url}', params={'appID':app_id, 'apiKey':api_key, 'stopNo':stopNo,'routeNo':busNo}).json()
    
    try:
        stop_times_info = res['GetNextTripsForStopResult']['Route']['RouteDirection']['Trips']['Trip']
    
        stop_times = []
        for time in stop_times_info:
            stop_times.append(time['TripStartTime'])

        u = get_username()
        return render_template ('next_bus.html', stop_times=stop_times, u=u)
    
    except:
        flash('Wrong bus or stop number','danger')
        u = get_username()
        return redirect('/next_bus')


@app.route('/report_late_bus', methods=['GET','POST'])
def report_late_bus():
    form = AddLateBusForm()
    validate = Validator()
    u = get_username()
    
    if form.validate_on_submit():
        stopNo = form.stopNo.data
        busNo = form.busNo.data
        scheduled_arrival = form.scheduled_arrival.data
        delay = form.delay.data
        noShow = form.no_show.data
        
        valide_schedule_time = validate.validate_schedule_time(scheduled_arrival)
        valide_submission = validate.validate_busNo_stopNo(busNo,stopNo)
        
        if valide_schedule_time and valide_submission:
            new_report = Submitted_Data(stopNo = stopNo, busNo = busNo, delay = delay, noShow = noShow, date_submitted = datetime.now() )

            db.session.add(new_report)
            db.session.commit()
       
            flash(f"Bus {busNo} from stop {stopNo} has been reported", 'success')
            return redirect("/")

        else:
            for err in validate.errors:
                flash(err, 'danger')
                
            return redirect('/report_late_bus')

    else:
        return render_template(
            "report_late_bus.html", form=form, u=u)

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)

        if user:

            session['user_id'] = user.id
                        
            flash(f"Welcome back {username}!", 'success')
            return redirect("/")
        else:
            flash(f"Wrong password / username combination", 'danger')
            return redirect('/login')

    else:
        u = get_username()
        return render_template(
            "login.html", form=form, u=u)
    


@app.route('/signup', methods=['GET','POST'])
def signup():

    form = SignUp()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
       
        alt = User.query.filter_by(username=username).first()
                
        if not alt:
            new_user = User.register(username, password)
            db.session.add(new_user)
            db.session.commit()
            
            session['user_id'] = new_user.id
            flash(f'Welcome {username}!', 'success')
            return redirect('/')

        else:
            flash(f'{username} already taken!', 'danger')
            redirect('/signup') 

    u = get_username()
    return render_template('signup.html', form = form, u=u)


@app.route('/logout', methods=['GET'])
def logout():

    if session['user_id']:
        session['user_id'] = None
        flash('Successfully logged out!', 'success')
        return redirect ('/')
    else:
        flash('You are not logged in!', 'info')
        return redirect('/login')

@app.route('/db_request', methods=['GET'])
def db_request():
    
    stops_arr = get_stopNo_from_gtfs_stops_text('gtfs/stops.txt')
    bus_arr = get_busNo_from_gtfs_routes_text('gtfs/routes.txt')

    req = request.args
    stopNo = req['stopNo']
    busNo = req['busNo']
    to_time = req['to_time']
    from_time = req['from_time']
    
    data = get_search_query_data(req)
    resp = extract_search_query_data(data, busNo,stopNo)


    raise


    
    
    
    print('%%%%%%%%%%%%%%%%%%%%%%%%')
    print(resp)
    print(busNo, stopNo)
    print('%%%%%%%%%%%%%%%%%%%%%%%%')

    return 'test'