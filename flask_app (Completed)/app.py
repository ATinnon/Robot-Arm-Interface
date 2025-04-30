from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__, template_folder="/home/atinnon/flask_app/templates", static_folder="/home/atinnon/flask_app/static")

@app.route("/")
def project_overview():
    return render_template("project_overview.html")

@app.route("/tutorial_tab.html")
def tutorial():
    return render_template("tutorial_tab.html")

@app.route("/program_tab.html")
def program():
    return render_template("program_tab.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/control", methods=["POST"])
def control_robot():
    data = request.json
    print("Received data:", data)
    
    motor_id = data.get("motor_id")
    raw_steps = data.get("steps")
    direction = data.get("direction")

    if motor_id is None or raw_steps is None or direction is None:
        return jsonify({"message": "Invalid data received"}), 400
        
        print(f"Processed Input - Motor: {motor_id}, Steps: {raw_steps}, Direction: {direction}")

    try:
        steps = int(raw_steps)
        abs_steps = abs(steps)
        direction = int(direction)
        
        print(f"Recieved Input - Motor: {motor_id}, Steps: {steps}, Direction: {direction}")
        print(f"Executing command: python3 /home/atinnon/robot_script_New.py {motor_id} {abs_steps} {direction}")

        
        result = subprocess.run(
            ["python3", "/home/atinnon/robot_script_New.py", str(motor_id), str(steps), str(direction)],
            capture_output=True,
            text=True
            )
            
        print(f"Subprocess return code: {result.returncode}")
        print(f"Subprocess stdout: {result.stdout}")
        print(f"Subprocess stderr: {result.stderr}")

        return f"Response: {result.stdout}"
        
        if result.returncode != 0:
            return jsonify({"status": "error", "message": "Script execution failed", "stderr": result.stderr})
        
        return jsonify({"status": "success", "output": result.stdout})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)})
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

