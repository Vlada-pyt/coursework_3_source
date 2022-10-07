from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Genre', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Comedy'),
})

director: Model = api.model('Director', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Sany'),
})

movie: Model = api.model('Movie', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Story'),
    'description': fields.String(required=True, max_length=100, example='description'),
    'trailer': fields.String(required=True, max_length=100, example='trailer'),
    'year': fields.Integer(required=True, example=1),
    'rating': fields.Float(required=True, example=1.2),
    'genre_id': fields.Integer(required=True, example=1),
    'director_id': fields.Integer(required=True, example=1),
    })

user: Model = api.model('User', {
    'id': fields.Integer(required=True, example=1),
    'email ': fields.String(required=True, max_length=100, example='email'),
    'password ': fields.String(required=True, max_length=100, example='password'),
    'name': fields.String( max_length=100, example='name'),
    'surname': fields.String(example='surname'),
    'favorite_genre': fields.String(example='favorite_genre'),
    })

