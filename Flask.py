from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from threading import Thread
import socket

app = Flask(__name__)
socketio = SocketIO(app)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error_message="Internal Server Error"), 500

drone_state = {
    'camera': None,
    'server_drone_coordinates': {'latitude': 32.34867703112118, 'longitude':  -6.342779389650304},
    'serverBatteryPercentage': 100,
    'return_home_enabled': False,
    'rth_coordinates': {'latitude': 0, 'longitude': 0},
    'headless_flight_mode': False,
    'guided_flight_mode': False,
    'power_on': False,
    'serverLeftJoystick' : {'degree' : 0,'percentage' : 0},
    'serverRightJoystick' : {'degree' : 0}
}


@socketio.on('analog_controls')
def analog_controls_thread():
    while drone_state['power_on']:
        if 'serverLeftJoystick' in drone_state:
            degree = drone_state['serverLeftJoystick'].get('degree', 0)
            percentage = drone_state['serverLeftJoystick'].get('percentage', 0)

            degree = (degree + 100) / 20
            percentage = (percentage + 100) / 20

            socketio.emit('serverLeftJoystick', serverLeftJoystick)

        time.sleep(0.1)
        if 'serverRightJoystick' in drone_state:
            degree = drone_state['serverRightJoystick'].get('degree', 0)
            degree = (degree + 180) % 360
            socketio.emit('serverRightJoystick', serverRightJoystick)

@socketio.on('camera_feed')
def handle_camera_feed(data):
    drone_state['camera'] = data
    if 'power_on' == True :
     socketio.emit('camera_feed', data)
     sleep (0.1)

@socketio.on('server_drone_coordinates')
def handle_server_drone_coordinates(data):
    drone_state['server_drone_coordinates'] = data
    socketio.emit('server_drone_coordinates', jsonify(data) )

    


@socketio.on('serverBatteryPercentage')
def handle_serverBatteryPercentage(data):
    drone_state['serverBatteryPercentage'] = data
    if 'power_on' == True :
     socketio.emit('serverBatteryPercentage', jsonify(data) )
     sleep (0.1)


@socketio.on('ping')
def handle_ping(data):
    if 'power_on' == True :
     socketio.emit('ping', data)
     sleep (0.1)

@app.route('/return_home', methods=['POST'])
def return_home():
    data = request.json
    is_rth_enabled = data.get('status')
    print (is_rth_enabled)
    if is_rth_enabled == True :
        pass
    if is_rth_enabled == False :
        pass
    return jsonify(is_rth_enabled)



@app.route('/land', methods=['POST'])
def land():
    data = request.json
    is_land = data.get('status')
    if is_land == True :
        print ('Landing enabled')
    if is_land == False :
        print ('Landing disabled')
    print (is_land)
    return jsonify(is_land)


@app.route('/toggle_headless_flight_mode', methods=['POST'])
def toggle_headless_flight_mode():
    drone_state['headless_flight_mode'] = not drone_state['guided_flight_mode']
    return jsonify({'headless_flight_mode': drone_state['headless_flight_mode']})

@app.route('/toggle_guided_flight_mode', methods=['POST'])
def toggle_guided_flight_mode():
    drone_state['guided_flight_mode'] = not drone_state['headless_flight_mode']
    return jsonify({'guided_flight_mode': drone_state['guided_flight_mode']})

@app.route('/change_rth_coordinates', methods=['POST'])
def change_rth_coordinates():
    data = request.json
    coordinates = data.get('coordinates')
    if not coordinates:
        return jsonify("New homepoint set")
    'rth_coordinates' == coordinates
    return jsonify("coordinates succefully changed to :" , coordinates)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle_start', methods=['POST'])
def start_state():
    data = request.json
    is_start = data.get('status')
    if is_start == True :
        'power_on' == True
        print ('Drone started')
    if is_start == False :
        'power_on' == False
        print ('Drone stopped')
    return jsonify(is_start)




if __name__ == '__main__':
    socketio.run(app) 