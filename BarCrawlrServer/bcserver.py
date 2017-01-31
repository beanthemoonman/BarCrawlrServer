from flask import Flask, jsonify, current_app, make_response, abort

from BarCrawlrServer.model.plan import plan

server = Flask(__name__)

plans = [
    plan('{"Name":"test_plan_1","Address":"Oceanic location","Location":[0,0],"Note":"Test plan for testing"}'),
    plan('{"Name":"test_plan_2","Address":"Oceanic location","Location":[0,0],"Note":"Second test plan for testing"}')
]

@server.route('/')
def index():
    return "Welcome to Bar Crawlr Server"

# Post a new plan to the plans list
@server.route('/plan', methods=['POST'])
def create_plan():
    if not request.json or not 'Name' in request.json:
        abort(400)
    plans.append(plan(request.json))
    return jsonify({'plan': plan}), 201

# Get all the plans from the plans list
@server.route('/plans', methods=['GET'])
def get_all_plans():
    s = "All Plans:\n"
    for plan in plans:
        s += "\t" + plan.jsonify() + "\n"
    return s

# Get a specific plan using a plan id number from plans list
@server.route('/plan/<int:plan_id>',methods=['GET'])
def get_plan(plan_id):
    if len(plans) < plan_id or plan_id < 0:
        abort(400)
    return plans[plan_id].jsonify()

# 404 Error Handler
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    server.run(debug=True)
