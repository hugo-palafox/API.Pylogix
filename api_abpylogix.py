import os
import logging
from pylogix import PLC
from flask import Flask, jsonify, request
from Models import PyLogixTag 
from Models import Tool
from Models import ToolAndPyLogixTagDTO
from datetime import datetime

app = Flask(__name__)

# Create the log directory if it doesn't exist
log_dir = "C:/Pylogix/log"
os.makedirs(log_dir, exist_ok=True)

# Define the log file path
log_file = os.path.join(log_dir, "app.log")

# Configure the logging settings to log to the specified file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Log to the specified file
        logging.StreamHandler()  # Log to console
    ]
)

@app.route('/api/gettaglist', methods=['GET'])
def get_tag_list():
    try:
        # Log incoming request information
        client_ip = request.remote_addr
        request_method = request.method
        request_url = request.url
        logging.info(f"Incoming request from {client_ip}: {request_method} {request_url}")

        tag_list = []
        with PLC() as comm:
            comm.ProcessorSlot = 1
            comm.IPAddress = '192.168.120.131'
            tags = comm.GetTagList()

            if tags is None:
                # Handle the case where no tags were retrieved
                error_message = "No tags found"
                logging.error(error_message)
                return jsonify({"error": error_message}), 404

            if tags.Value is not None:
                for tag in tags.Value:
                    # Instantiate ListTag objects and add them to the list
                    tag_obj = PyLogixTag(tag.TagName, tag.DataType)  # Use the correct attribute names
                    tag_list.append({
                        "Name": tag_obj.Name,
                        "Type": tag_obj.Type
                    })

       
        logging.info("Successfully retrieved tags.")
        return jsonify(tag_list)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500



@app.route('/api/gettaglist/v2', methods=['POST'])
def get_tag_listv2():
    try:
        # Log incoming request information
        client_ip = request.remote_addr
        request_method = request.method
        request_url = request.url
        logging.info(f"Incoming request from {client_ip}: {request_method} {request_url}")

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided in the request body"}), 400
        # Create instance
        tool = Tool(**data)
        slot=tool.RackSlot.split(",")[1].strip()
        result = []
        tag_list = []

        with PLC() as comm:
            comm.ProcessorSlot = slot
            comm.IPAddress = tool.IpAddress#'192.168.120.132'
            tags = comm.GetTagList()

            if tags is None:
                # Handle the case where no tags were retrieved
                error_message = "No tags found"
                logging.error(error_message)
                return jsonify({"error": error_message}), 404

            if tags.Value is not None:
                for tag in tags.Value:
                    # Instantiate ListTag objects and add them to the list
                    #tag_obj = PyLogixTag(tag.TagName:, tag.DataType)  # Use the correct attribute names
                    tag_list.append({
                        "Name": tag.TagName,
                        "Type": tag.DataType,
                        "TypeValue":tag.DataTypeValue,
                        "Value":"",
                        "TimeStamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    })

       
        logging.info("Successfully retrieved tags.")
        return jsonify(tag_list)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500


@app.route('/api/readtags', methods=['POST'])
def read_tags():
    try:
        # Log incoming request information
        client_ip = request.remote_addr
        request_method = request.method
        request_url = request.url
        logging.info(f"Incoming request from {client_ip}: {request_method} {request_url}")

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided in the request body"}), 400
        
        # Create instances of Tool and PyLogixTag
        tool_data = data.get('ToolData')
        tool = Tool(**tool_data)
        tags_data = data.get('PyLogixTags')
         

        slot = tool.RackSlot.split(",")[0].strip()        
        tag_list = []

        with PLC() as comm:
            comm.ProcessorSlot = slot
            comm.IPAddress = tool.IpAddress#'192.168.120.132'

            for tag_data in tags_data:
                tag = PyLogixTag(
                    Name=tag_data.get("Name"),
                    Type=tag_data.get("Type"),
                    TypeValue=tag_data.get("TypeValue"),
                    Status=tag_data.get("Status"),
                    Value=tag_data.get("Value"),
                    TimeStamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                )
                tag_read = comm.Read(tag.Name)#, datatype=tag.TypeValue
                tag_list.append({
                    "Name": tag.Name,
                    "Type": tag.Type,
                    "TypeValue":tag.TypeValue,
                    "Status":tag_read.Status,
                    "Value": tag_read.Value,
                    "TimeStamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                })

            if tags_data is None:
                # Handle the case where no tags were retrieved
                error_message = "No tags found"
                logging.error(error_message)
                return jsonify({"error": error_message}), 404


        logging.info("Successfully retrieved tags.")
        return jsonify(tag_list)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(port=8080)  # Run on port 8080
