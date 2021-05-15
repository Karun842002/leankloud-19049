from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from utils import TodoDAO
import databas

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API', description='A simple TodoMVC API')
ns = api.namespace('todos', description='TODO operations')
todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'dueby': fields.Date(required=True, description='The task date'),
    'status': fields.String(required=True, description='The task status')
})


DAO = TodoDAO()

@ns.route('/')
class TodoList(Resource):
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        return DAO.getall()

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        return DAO.update(id, api.payload)

@ns.route('/due')
@ns.param('due_date','')
class DueList(Resource):
    @ns.doc('get_due_todo')
    @ns.marshal_list_with(todo)
    def get(self, due_date):
        return databas.due()

@ns.route('/due')
@ns.param('due_date','')
class OverdueList(Resource):
    @ns.doc('get_due_todo')
    @ns.marshal_list_with(todo)
    def get(self, due_date):
        return databas.overdue()

@ns.route('/due')
@ns.param('due_date','') 
class FinishedList(Resource):
    @ns.doc('get_due_todo')
    @ns.marshal_list_with(todo)
    def get(self, due_date):
        return databas.finished()

if __name__ == '__main__':
    app.run()
