from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data from JSON file
with open('data.json') as f:
    data = json.load(f)

# Counter for number of times each provider has been returned
result_counts = {provider['id']: 0 for provider in data}


# Read by id endpoint
@app.route('/data/<int:data_id>', methods=['GET'])
def get_data_by_id(data_id):
    for provider in data:
        if provider['id'] == data_id:
            # Increment counter for provider
            result_counts[data_id] += 1
            return jsonify(provider)
    return jsonify({'error': 'Data not found.'}), 404


# List endpoint with optional query parameters
@app.route('/data', methods=['GET'])
def get_data_list():
    result_data = []
    for provider in data:
        # Filter based on query parameters
        match = True
        for param, value in request.args.items():
            # Filter properties that are lists
            if isinstance(provider[param], list):
                if value not in provider[param]:
                    match = False
                    break
            # Filter properties that are string/basic types
            else:
                if str(provider[param]).lower() != str(value).lower():
                    match = False
                    break
        # If provider makes it past all the filtering add it and increment result count with its id
        if match:
            result_data.append(provider)
            result_counts[provider['id']] += 1

    # Sort results by number of times each provider has been returned and rating
    result_data = sorted(result_data, key=lambda sorted_provider: (
        -sorted_provider['rating'], -result_counts[sorted_provider['id']]))

    return jsonify(result_data)


if __name__ == '__main__':
    app.run(debug=True)
