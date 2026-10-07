import http.server
import socketserver
import webbrowser
import json
import urllib.parse
from datetime import datetime
import database

PORT = 5000

class BMIAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. API: Get all unique users
        if path == "/api/users":
            try:
                users = database.get_all_users()
                self.send_json_response(200, {"users": users})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        # 2. API: Get records for a specific user
        elif path == "/api/records":
            params = urllib.parse.parse_qs(parsed.query)
            user_name = params.get("user", [""])[0]
            try:
                records = database.get_records_by_user(user_name) if user_name else []
                # records format: list of tuples (id, user_name, weight, height, bmi, category, created_at)
                data = [
                    {
                        "id": r[0],
                        "user_name": r[1],
                        "weight": r[2],
                        "height": r[3],
                        "bmi": r[4],
                        "category": r[5],
                        "created_at": r[6]
                    }
                    for r in records
                ]
                self.send_json_response(200, {"records": data})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        # 3. Default: Serve index.html or static files
        if path == "/" or path == "":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. API: Save a new BMI record
        if path == "/api/calculate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
                user_name = payload.get("user_name", "").strip()
                weight = float(payload.get("weight", 0))
                height = float(payload.get("height", 0))

                if not user_name:
                    self.send_json_response(400, {"error": "User name is required."})
                    return
                if weight <= 0 or height <= 0:
                    self.send_json_response(400, {"error": "Weight and height must be positive numbers."})
                    return

                # Calculate BMI
                bmi = weight / (height ** 2)

                # Classify
                if bmi < 18.5:
                    category = "Underweight"
                elif 18.5 <= bmi < 25:
                    category = "Normal weight"
                elif 25 <= bmi < 30:
                    category = "Overweight"
                else:
                    category = "Obese"

                # Save to SQLite database
                database.save_record(user_name, weight, height, bmi, category)

                self.send_json_response(200, {
                    "user_name": user_name,
                    "weight": weight,
                    "height": height,
                    "bmi": round(bmi, 2),
                    "category": category,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                self.send_json_response(500, {"error": f"Server error: {e}"})
            return

        # 2. API: Delete record
        elif path == "/api/delete":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
                record_id = payload.get("id")
                database.delete_record(record_id)
                self.send_json_response(200, {"success": True})
            except Exception as e:
                self.send_json_response(500, {"error": str(e)})
            return

        self.send_json_response(404, {"error": "Not found"})

    def send_json_response(self, status_code, data):
        """Helper to send structured JSON responses."""
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

def run_server():
    # Make sure SQLite table exists
    database.init_db()

    # Reuse address to prevent 'Address already in use' errors
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BMIAppHandler) as httpd:
        url = f"http://127.0.0.1:{PORT}"
        print("=" * 60)
        print("       BMI HEALTH TRACKER WEB SERVER")
        print("=" * 60)
        print(f"Server is running live at: {url}")
        print("Opening in your web browser...")
        print("Press Ctrl + C in this terminal to stop the server.")
        print("=" * 60)

        # Automatically pop up the web browser
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully. Goodbye!")

if __name__ == "__main__":
    run_server()
