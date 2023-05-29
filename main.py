from flask import Flask, request, jsonify
import traceback
from Facade import Facade
from Utils.Urgency import Urgency

app = Flask("BuilderAPI")
facade: Facade = Facade()

ERROR_CODE = None


@app.route("/register", methods=["POST"])
def handle_request_register():
    print("Register request received")

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
    print("Login request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        result = facade.login(data["username"], data["password"])
        return jsonify({"result": result})
    except Exception as e:
        print(f"[login] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/logout", methods=["POST"])
def handle_request_logout():
    print("Logout request received")

    # Parse JSON payload from the request
    data = request.get_json()
    print(f"data : {data}")

    # Call the facade method
    try:
        facade.logout(data["username"])
        return jsonify({"result": "success"})
    except Exception as e:
        print(f"[logout] : raised exception {str(e)}")
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/add_project", methods=["POST"])
def handle_request_add_project():
    print("Add Project request received")

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
def handle_request_add_stage():
    print("Add Stage request received")

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
def handle_request_add_mission():
    print("Add Mission request received")

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
def handle_request_edit_project_name():
    print("Edit Project Name request received")

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
def handle_request_edit_stage_name():
    print("Edit Stage Name request received")

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
def handle_request_edit_mission_name():
    print("Edit Mission Name request received")

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
def handle_request_set_mission_status():
    print("Set Mission Status request received")

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
def handle_request_get_all_missions():
    print("Get All Missions request received")

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
def handle_request_get_all_stages():
    print("Get All Stages request received")

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
def handle_request_assign_project_to_user():
    print("Assign Project To User request received")

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
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/edit_comment_in_mission", methods=["POST"])
def handle_request_edit_comment_in_mission():
    print("Edit Comment In Mission request received")

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
def handle_request_remove_stage():
    print("Remove Stage request received")

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
def handle_request_remove_mission():
    print("Remove Mission request received")

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
        return jsonify({"error": str(e)}), ERROR_CODE


@app.route("/set_green_building", methods=["POST"])
def handle_request_set_green_building():
    print("Set Green Building request received")

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
def handle_request_set_stage_status():
    print("Set Stage Status request received")

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
def handle_request_get_all_assigned_users_in_project():
    print("Get All Assigned Users In Project request received")

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
def handle_request_set_urgency():
    print("Set Urgency request received")

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
def handle_request_add_building_fault():
    print("Add Building Fault request received")

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
def handle_request_remove_building_fault():
    print("Remove Building Fault request received")

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
def handle_request_set_build_fault_status():
    print("Set Build Fault Status request received")

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
def handle_request_remove_user_from_project():
    print("Remove User From Project request received")

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
def handle_request_get_my_permission():
    print("Get my permission request received")

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
    print("Echo request received")

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
def handle_request_get_projects():
    print("get projects received")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
