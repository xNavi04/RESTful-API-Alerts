How to use my REST API (FOR PYTHON 3.10)
---> https://documenter.getpostman.com/view/31260362/2s9Ykhi5En#000f6483-52c1-4e48-bf71-3a2344408cbf




**Add Alert:**

This script utilizes the requests library in Python to send a POST request to a specified URL (http://127.0.0.1:5000/add). It adds an alert with a name (required) and an optional description. The requirements state that the name is mandatory, but the description is optional.

**Get All Alerts:**

This script sends a GET request to http://127.0.0.1:5000/all with parameters including a password, alert name, and description. It retrieves all alerts based on the provided criteria. The requirements specify that both the name and password are required, while the description is optional.

**Display Single Alert:**

By sending a GET request to http://127.0.0.1:5000/display_one with the name parameter, this script retrieves information about a specific alert. The usage indicates that you need to input the alert name to get details about that particular alert.

**Edit Alert Description:**

This script sends a PATCH request to http://127.0.0.1:5000/edit_description/{alert_id} to edit the description of a specific alert. It requires providing a password and the new alert description. The usage specifies that you should input the new alert description to perform the edit, and a valid password is required.

**Send SMS Alert:**

Using a POST request to http://127.0.0.1:5000/send_sms_alert/{alert_id}, this script sends an SMS alert to a specified user. It requires a password and the recipient's phone number. The usage indicates that you need to send an SMS with the alert to the specified user, and both a valid password and the user's phone number are necessary.






