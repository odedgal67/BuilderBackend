from datetime import timedelta

from flask_session import Session
from typing import Callable

from functools import wraps
from flask import Flask, request, jsonify, abort, send_from_directory, session

import traceback

from Config import GLOBAL_CONFIG
from DTO.UserDTO import UserDTO
from Facade import Facade
from User import User
from Utils.Urgency import Urgency
import os
import secrets

from db_utils import my_collection

app = Flask("BuilderAPI")
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
secret_key = secrets.token_hex(32)  # Generate a 32-byte secret key
app.secret_key = secret_key
Session(app)
app.permanent_session_lifetime = timedelta(minutes=10)
facade: Facade = Facade()

ERROR_CODE = None
REFRESH_TOKEN_ERROR_CODE = 401



def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "User not logged in (no current session)"}), REFRESH_TOKEN_ERROR_CODE
        return func(*args, **kwargs)
    return wrapper

@app.route("/register", methods=["POST"])
def handle_request_register():
    print("\n\nRegister request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.register(data["username"], data["password"], data["name"])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[register] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/login", methods=["POST"])
def handle_request_login():
    print("\n\nLogin request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.login(data["username"], data["password"])
        session['user_id'] = data["username"]
        return jsonify({"result": result})
    except Exception as e:
        print(f"[login] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/logout", methods=["POST"])
def handle_request_logout():
    print("\n\nLogout request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.logout(data["username"])
        session.clear()
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[logout] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_project", methods=["POST"])
@require_login
def handle_request_add_project():
    print("\n\nAdd Project request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.add_project(data["project_name"], data["username"])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[add_project] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_stage", methods=["POST"])
@require_login
def handle_request_add_stage():
    print("\n\nAdd Stage request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.add_stage(
            data["project_id"],
            data["title_id"],
            data["stage_name"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[add_stage] : raised exception {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_mission", methods=["POST"])
@require_login
def handle_request_add_mission():
    print("\n\nAdd Mission request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.add_mission(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["mission_name"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[add_mission] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_project_name", methods=["POST"])
@require_login
def handle_request_edit_project_name():
    print("\n\nEdit Project Name request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_project_name(
            data["project_id"], data["new_project_name"], data["username"]
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_project_name] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_stage_name", methods=["POST"])
@require_login
def handle_request_edit_stage_name():
    print("\n\nEdit Stage Name request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_stage_name(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["new_stage_name"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_stage_name] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_mission_name", methods=["POST"])
@require_login
def handle_request_edit_mission_name():
    print("\n\nEdit Mission Name request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_mission_name(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["mission_id"],
            data["new_mission_name"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_mission_name] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/set_mission_status", methods=["POST"])
@require_login
def handle_request_set_mission_status():
    print("\n\nSet Mission Status request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.set_mission_status(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["mission_id"],
            data["new_status"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[set_mission_status] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_all_missions", methods=["POST"])
@require_login
def handle_request_get_all_missions():
    print("\n\nGet All Missions request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_all_missions(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_all_missions] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_all_stages", methods=["POST"])
@require_login
def handle_request_get_all_stages():
    print("\n\nGet All Stages request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_all_stages(
            data["project_id"],
            data["title_id"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_all_stages] : raised exception {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/assign_project_to_user", methods=["POST"])
@require_login
def handle_request_assign_project_to_user():
    print("\n\nAssign Project To User request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.assign_project_to_user(
            data["project_id"],
            data["permission_type"],
            data["assigning_username"],
            data["username_to_assign"],
        )
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[assign_project_to_user] : raised exception {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_comment_in_mission", methods=["POST"])
@require_login
def handle_request_edit_comment_in_mission():
    print("\n\nEdit Comment In Mission request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_comment_in_mission(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["mission_id"],
            data["comment"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_comment_in_mission] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/remove_stage", methods=["POST"])
@require_login
def handle_request_remove_stage():
    print("\n\nRemove Stage request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.remove_stage(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[remove_stage] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/remove_mission", methods=["POST"])
@require_login
def handle_request_remove_mission():
    print("\n\nRemove Mission request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.remove_mission(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["mission_id"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[remove_mission] : raised exception {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/set_green_building", methods=["POST"])
@require_login
def handle_request_set_green_building():
    print("\n\nSet Green Building request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.set_green_building(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["mission_id"],
            data["is_green_building"],
            data["username"],
            data.get("apartment_number", None),
        )
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[set_green_building] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/set_stage_status", methods=["POST"])
@require_login
def handle_request_set_stage_status():
    print("\n\nSet Stage Status request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.set_stage_status(
            data["project_id"],
            data["title_id"],
            data["stage_id"],
            data["new_status"],
            data["username"],
        )
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[set_stage_status] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_all_assigned_users_in_project", methods=["POST"])
@require_login
def handle_request_get_all_assigned_users_in_project():
    print("\n\nGet All Assigned Users In Project request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_all_assigned_users_in_project(
            data["project_id"], data["username"]
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_all_assigned_users_in_project] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/set_urgency", methods=["POST"])
@require_login
def handle_request_set_urgency():
    print("\n\nSet Urgency request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.set_urgency(
            data["project_id"],
            data["building_fault_id"],
            data["new_urgency"],
            data["username"],
        )
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[set_urgency] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_building_fault", methods=["POST"])
@require_login
def handle_request_add_building_fault():
    print("\n\nAdd Building Fault request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.add_building_fault(
            data["project_id"],
            data["name"],
            data["username"],
            data["floor_number"],
            data["apartment_number"],
            data.get("urgency", Urgency.LOW),
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[add_building_fault] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/remove_building_fault", methods=["POST"])
@require_login
def handle_request_remove_building_fault():
    print("\n\nRemove Building Fault request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.remove_building_fault(
            data["project_id"], data["build_fault_id"], data["username"]
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[remove_building_fault] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/set_build_fault_status", methods=["POST"])
@require_login
def handle_request_set_build_fault_status():
    print("\n\nSet Build Fault Status request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.set_build_fault_status(
            data["project_id"],
            data["build_fault_id"],
            data["new_status"],
            data["username"],
        )
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[set_build_fault_status] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/remove_user_from_project", methods=["POST"])
@require_login
def handle_request_remove_user_from_project():
    print("\n\nRemove User From Project request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.remove_user_from_project(
            data["project_id"], data["username_to_remove"], data["removing_user"]
        )
        return jsonify({"result": result})
    except Exception as e:
        print(f"[remove_user_from_project] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_my_permission", methods=["POST"])
@require_login
def handle_request_get_my_permission():
    print("\n\nGet my permission request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_my_permission(
            data["project_id"],
            data["username"],
        )
        print(jsonify({"result": result}))
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_my_permission] : raised exception {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/echo", methods=["POST"])
def handle_request_echo():
    print("\n\nEcho request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = {"echo": data["echo_string"]}
        return jsonify({"result": result})
    except Exception as e:
        print(f"[echo] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_projects", methods=["POST"])
@require_login
def handle_request_get_projects():
    print("\n\nget projects received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_projects(data["username"])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_projects] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE

def get_attributes_on_set_file_request(request):
    data = request.files.get('file')
    original_file_name = request.form.get('file_name')
    project_id = request.form.get('project_id')
    apartment_number = request.form.get('apartment_number')
    stage_id = request.form.get('stage_id')
    mission_id = request.form.get('mission_id')
    username = request.form.get('username')
    title_id = request.form.get('title_id')
    return data, original_file_name, project_id, apartment_number, stage_id, mission_id, username, title_id

def wrap_with_try_except(func_name: str, func: Callable, *kwargs):
    try:
        result = func(*kwargs)
        return jsonify({"result": result})
    except Exception as e:
        print(f"[{func_name}] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE

@app.route("/set_mission_proof", methods=['POST'])
@require_login
def handle_set_mission_proof():
    print("set mission proof request received")
    data, original_file_name, project_id, apartment_number, stage_id, mission_id, username, title_id = get_attributes_on_set_file_request(request)
    return wrap_with_try_except("set_mission_proof", facade.set_mission_proof, project_id, int(title_id), stage_id, mission_id, data.read(), original_file_name, username, apartment_number)

@app.route('/set_mission_tekken', methods=['POST'])
@require_login
def handle_set_mission_tekken():
    print("set mission proof request received")
    data, original_file_name, project_id, apartment_number, stage_id, mission_id, username, title_id = get_attributes_on_set_file_request(request)
    return wrap_with_try_except("set_mission_tekken", facade.set_mission_tekken, project_id, int(title_id), stage_id, mission_id, data.read(), original_file_name, username, apartment_number)

@app.route('/set_mission_plan_link', methods=['POST'])
@require_login
def handle_set_mission_plan_link():
    print("post set_mission_plan_link request recieved")
    data, original_file_name, project_id, apartment_number, stage_id, mission_id, username, title_id = get_attributes_on_set_file_request(request)
    return wrap_with_try_except("set_mission_plan_link", facade.set_mission_plan_link, project_id, int(title_id), stage_id, mission_id, data.read(), original_file_name, username, apartment_number)



@app.route('/<path:filename>', methods=['GET'])
# @require_login
def serve_file(filename):
    file_path = os.path.join(GLOBAL_CONFIG.SERVER_FILE_DIRECTORY, filename)

    if not os.path.isfile(file_path):
        print(f"file not found on get request {file_path}")
        abort(404)

    return send_from_directory(GLOBAL_CONFIG.SERVER_FILE_DIRECTORY, filename)


@app.route("/get_all_building_faults", methods=["POST"])
@require_login
def handle_request_get_all_building_faults():
    print("get all building faults request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_all_building_faults(data['project_id'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_all_building_faults] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_plan", methods=["POST"])
@require_login
def handle_request_add_plan():
    print("\n\nadd plan request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.add_plan(data['project_id'], data['plan_name'], data.get('link', ""), data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[add_plan] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/remove_plan", methods=["POST"])
@require_login
def handle_request_remove_plan():
    print("\n\nremove plan request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.remove_plan(data['project_id'], data['plan_id'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[remove_plan] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_plan_name", methods=["POST"])
@require_login
def handle_request_edit_plan_name():
    print("\n\nedit plan name request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_plan_name(data['project_id'], data['plan_id'], data['new_plan_name'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_plan_name] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_plan_link", methods=["POST"])
@require_login
def handle_request_edit_plan_link():
    print("\n\nedit plan link request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_plan_link(data['project_id'], data['plan_id'], data['new_link'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_plan_link] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_mission_link", methods=["POST"])
@require_login
def handle_request_edit_mission_link():
    print("\n\nedit mission link request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.edit_mission_link(data['project_id'], data['title_id'], data['stage_id'], data['mission_id'], data['new_link'], data['username'], data.get('apartment_number', None))
        return jsonify({"result": result})
    except Exception as e:
        print(f"[edit_mission_link] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/change_user_permission_in_project", methods=["POST"])
@require_login
def handle_request_change_user_permission_in_project():
    print("\n\nchange user permission in project request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.change_user_permission_in_project(data['project_id'], data['new_permission'], data['username_to_change'], data['username_changing'])
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[change_user_permission_in_project] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/change_user_name", methods=["POST"])
@require_login
def handle_request_change_user_name():
    print("\n\nchange user name request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.change_user_name(data['new_name'], data['username_to_change'])
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[change_user_name] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/change_user_password", methods=["POST"])
@require_login
def handle_request_change_user_password():
    print("\n\nchange user password request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.change_user_password(data['new_password'], data['username_to_change'])
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[change_user_password] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_apartment", methods=["POST"])
@require_login
def handle_request_add_apartment():
    print("\n\nadd apartment request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.add_apartment(data['project_id'], data['apartment_number'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[add_apartment] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/remove_apartment", methods=["POST"])
@require_login
def handle_request_remove_apartment():
    print("\n\nremove apartment request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.remove_apartment(data['project_id'], data['apartment_number'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[remove_apartment] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_all_apartments_in_project", methods=["POST"])
@require_login
def handle_request_get_all_apartments_in_project():
    print("\n\nget all apartments in project request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_all_apartments_in_project(data['project_id'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_all_apartments_in_project] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/get_all_plans", methods=["POST"])
@require_login
def handle_request_get_all_plans():
    print("\n\nget all plans request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.get_all_plans(data['project_id'], data['username'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[get_all_plans] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_building_fault", methods=["POST"])
@require_login
def handle_request_edit_building_fault():
    print("\n\nedit building fault request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.edit_building_fault(data['project_id'], data['building_fault_id'], data['building_fault_name'], data['floor_number'], data['apartment_number'], data['green_building'], data['urgency'], data['proof_fix'], data['tekken'], data['plan_link'], data['status'], data['proof'], data['comment'], data['username'])
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[edit_building_fault] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


if __name__ == "__main__":
    print("running with the following configuration:")
    print(GLOBAL_CONFIG)
    facade.controller.read_database(my_collection.find())
    app.run(host=GLOBAL_CONFIG.IP, port=GLOBAL_CONFIG.PORT)
