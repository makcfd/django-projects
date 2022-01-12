from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

# first to do is to create an app

app = Flask(__name__)
# wrapping our app into API
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# creating and init db. Do it once
#db.create_all()

# validate put request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video")
video_put_args.add_argument("likes", type=int, help="Likes of the video")
video_put_args.add_argument("views", type=int, help="Views of the video")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")

resourse_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

# inheriting from Resource will allow to handle requests GET, DELETE, PUT and so on
class Video(Resource):
    @marshal_with(resourse_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Couldn't find video with such id...")
        return result

    @marshal_with(resourse_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="id taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resourse_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Couldn't find video with such id...")
        args = video_update_args.parse_args()
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]
        #db.session.add(result)
        db.session.commit()
        return result

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204



# registering a resource
# how do we find resourse when server was called on "/helloworld" url

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    # start server and app
    app.run(debug=True)
