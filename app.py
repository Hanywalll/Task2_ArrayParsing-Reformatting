from flask import Flask, request, jsonify

app = Flask(__name__)

def reformat_array(data):
    if not isinstance(data, list):
        return {"error": "Input harus berupa array dari dictionaries."}, 400

    reformatted_data = {}
    
    for item in data:
        category = item.get('category')
        sub_category = item.get('sub_category')
        
        if not category or not sub_category:
            continue
        
        if category not in reformatted_data:
            reformatted_data[category] = {}
        
        if sub_category not in reformatted_data[category]:
            reformatted_data[category][sub_category] = []
        
        new_item = {key: value for key, value in item.items() if key not in ['category', 'sub_category']}
        
        reformatted_data[category][sub_category].append(new_item)
        
    return reformatted_data

@app.route('/reformat', methods=['POST'])
def handle_reformat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data JSON tidak ditemukan dalam request."}), 400
        
        reformatted_output = reformat_array(data)
        
        if isinstance(reformatted_output, tuple):
            return jsonify(reformatted_output[0]), reformatted_output[1]
            
        return jsonify(reformatted_output), 200

    except Exception as e:
        return jsonify({"error": "Terjadi kesalahan pada server.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)