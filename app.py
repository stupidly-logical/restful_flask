from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

NODES = {
    'node1': {'status': 'offline'},
    'node2': {'status': 'offline'},
    'node3': {'status': 'online'},
}


def abort_if_node_doesnt_exist(node_id):
    if node_id not in NODES:
        abort(404, message="Node {} doesn't exist".format(node_id))

parser = reqparse.RequestParser()
parser.add_argument('node')

class ApiRoot(Resource):
    def get(self):
        return {'api_status':'online'}

# Todo
# shows a single todo item and lets you delete a todo item
class Node(Resource):
    def get(self, node_id):
        abort_if_node_doesnt_exist(node_id)
        return NODES[node_id]

    def delete(self, node_id):
        abort_if_node_doesnt_exist(node_id)
        del NODES[node_id]
        return '', 204

    def put(self, node_id):
        args = parser.parse_args()
        node = {'node': args['node']}
        NODES[node_id] = node
        return node, 201


# NodeList
# shows a list of all nodes, and lets you POST to add new nodes
class NodeList(Resource):
    def get(self):
        return NODES

    def post(self):
        args = parser.parse_args()
        node_id = int(max(NODES.keys()).lstrip('node')) + 1
        node_id = 'node%i' % node_id
        NODES[node_id] = {'node': args['node']}
        return NODES[node_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(ApiRoot, '/')
api.add_resource(NodeList, '/nodes')
api.add_resource(Node, '/nodes/<node_id>')


if __name__ == '__main__':
    app.run(debug=True)
