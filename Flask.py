from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

drone_state = {
    'camera': None,
    'serverDroneCoordinates': {'Circle_Value_angle_R': 0, 'Circle_Value_angle_L': 0},
    'serverBatteryPercentage': 100,
    'return_home_enabled': False,
    'rth_serverDroneCoordinates': {'latitude': 0, 'longitude': 0},
    'headless_flight_mode': False,
    'guided_flight_mode': False,
    'power_on': False,
    'serverLeftJoystick' : {degree : 0,percentage : 0},
    'serverRightJoystick' : {degree : 0}
}

def analog_controls_thread():
    while drone_state['power_on']:
        if 'serverLeftJoystick' in drone_state:
            degree = drone_state['serverLeftJoystick'].get('degree', 0)
            percentage = drone_state['serverLeftJoystick'].get('percentage', 0)

            # Convert values to 0-10 m/s range
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
    socketio.emit('camera_feed', data)

@socketio.on('serverDroneCoordinates')
def handle_serverDroneCoordinates(data):
    drone_state['serverDroneCoordinates'] = data
    socketio.emit('serverDroneCoordinates', data)

@socketio.on('serverBatteryPercentage')
def handle_serverBatteryPercentage(data):
    drone_state['serverBatteryPercentage'] = data
    socketio.emit('serverBatteryPercentage', data)

@socketio.on('analog_controls')
def handle_analog_controls(data):
    socketio.emit('analog_controls', data)

@app.route('/return_home', methods=['POST'])
def return_home():
    drone_state['return_home_enabled'] = True
    return jsonify({'message': 'Return Home initiated'})

@app.route('/land', methods=['POST'])
def land():
    return jsonify({'message': 'Landing initiated'})

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
    data = request.get_json()
    drone_state['rth_coordinates']['latitude'] = data.get('latitude', 0)
    drone_state['rth_coordinates']['longitude'] = data.get('longitude', 0)
    return jsonify({'message': 'RTH coordinates changed'})

@app.route('/toggle_power', methods=['POST'])
def power_on():
    drone_state['power_on'] = not drone_state['power_off']
    return jsonify({'power_on': drone_state['power_on']})
def power_off():
    drone_state['power_on'] = False
    return jsonify({'power_off': drone_state['power_off']})

def receive_data_from_external_app(data):
    if 'camera' in data:
        handle_camera_feed(data['camera'])
    if 'serverDroneCoordinates' in data:
        handle_serverDroneCoordinates(data['serverDroneCoordinates'])
    if 'serverBatteryPercentage' in data:
        handle_serverBatteryPercentage(data['serverBatteryPercentage'])
    if 'analog_controls' in data:
        handle_analog_controls(data['analog_controls'])

if __name__ == '__main__':
    socketio.run(app)