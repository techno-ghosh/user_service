from flask import Flask, jsonify, request

app = Flask(__name__)



users = {
        '1': {'name': 'Alice', 'email': 'alice@example.com'},
        '2': {'name': 'Bob', 'email': 'bob@example.com'}
    }

@app.route('/')
def hello():
    return users

@app.route('/user/<id>')
def user(id):
    
    user_info = users.get(id, {})
    if(len(user_info.keys())) == 0:
        # try once more with string user id
        string_user_info = users.get(str(id),{})
        if(len(string_user_info.keys()) == 0):
            return 'No user found',404
        else:
            return jsonify(string_user_info) 
    else:
        return jsonify(user_info)




# CREATE OPERATION
@app.route('/user/add',methods=['POST'])
def create():
    
    if(request.json['name'] and request.json['email']):
        # code here
        if(request.json['email'] !='' and request.json['name'] != ''):
    
            email = request.json['email']
            name = request.json['name']
            
            
            new_key = int(sorted(users.keys())[-1]) + 1

            users[f'{new_key}'] = {
                "user_id" : new_key,
                "email" : email,
                "name" : name
            }
            return jsonify(users)
        else:
            return 'parameters missing'
    else:
        return 'parameteres missing'


# UPDATE OPERATION
@app.route('/user/update_user', methods=['PUT', 'POST'])
def update():
    if(request.method == 'POST' or request.method == 'PUT'):
        
        if(request.json['user_id']):
            if(users.get(str(request.json['user_id']), {})):
                user_id = str(request.json['user_id'])
                email = request.json['email']
                name = request.json['name']
                    
                users[f'{user_id}'] = {
                    "user_id" : user_id,
                    "email" : email,
                    "name" : name
                }
                return users[f'{user_id}']
            else: 
                return "user not found"
        else:
            return 'User not found'
        
    else:
        return 'method not allowed',403

# DELETE OPERATION

@app.route('/user/delete_user', methods=['DELETE'])
def delete():
    
   
    if(request.method == 'DELETE'):
        
        if(users.get(str(request.json['user_id']), {})):
            
            users.pop(str(request.json['user_id']))        
            return {
                "message" : "user deleted",
                "remaninig_users" : users
            }
        else:
            return 'user does not exist'
    else:
        return 'method not allowed',403





if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)