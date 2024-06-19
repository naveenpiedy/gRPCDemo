# Created by NaveenPiedy at 6/18/2024 6:32 AM
import pprint
from concurrent import futures

import grpc
import logging

import movies_management_pb2
import movies_management_pb2_grpc
from db_mimic import movies_db, actors_db, Movie, Actor

VALID_API_KEY = "secret-api-key"


class MoviesService(movies_management_pb2_grpc.MoviesServiceServicer):

    @staticmethod
    def get_metadata(context):
        """
        Returns metadata of the request
        """
        return dict(context.invocation_metadata())

    @staticmethod
    def validate_api_key(metadata, context):
        """
        Validates API key from metadata
        """
        api_key = metadata.get('api-key')
        trace_id = metadata.get('trace-id')

        if api_key != VALID_API_KEY:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid API key")
            logging.warning(f"Invalid API key for trace ID: {trace_id}")
            return False
        return True

    @staticmethod
    def log_trace(metadata, message):
        """
        Logs trace message
        """
        trace_id = metadata.get('trace-id', 'unknown')
        logging.info(f"Trace ID: {trace_id} - {message}")

    def GetMovie(self, request, context):
        """
        Get movie details from database.
        """
        metadata = self.get_metadata(context)
        self.log_trace(metadata, f"Received request for movie: {request.name}")

        if not self.validate_api_key(metadata, context):
            return movies_management_pb2.MovieResponse()

        try:
            movie_name = request.name
            sanitized_movie_name = movie_name.lower()
            if sanitized_movie_name in movies_db:
                result_movie = movies_db.get(sanitized_movie_name)
                return movies_management_pb2.MovieResponse(
                    id=result_movie.id,
                    name=result_movie.name,
                    actors=result_movie.actors,
                    director=result_movie.director,
                    rating=result_movie.rating
                )
            else:
                # Movie not in database
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Movie not found')
                return movies_management_pb2.MovieResponse()
        except Exception as e:
            self.log_trace(metadata, f"Error while getting movie: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal server error')
            return movies_management_pb2.MovieResponse()

    def GetActor(self, request, context):
        """
        Returns Actor details
        """
        metadata = self.get_metadata(context)
        self.log_trace(metadata, f"Received request for actor: {request.actor_name}")

        if not self.validate_api_key(metadata, context):
            return movies_management_pb2.MovieResponse()

        try:
            actor_name = request.actor_name
            sanitized_actor_name = actor_name.lower()
            if sanitized_actor_name in actors_db:
                result_actor = actors_db.get(sanitized_actor_name)
                return movies_management_pb2.ActorResponse(
                    id=result_actor.id,
                    actor_name=result_actor.actor_name,
                    movie_names=result_actor.movie_names
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Actor not in system')
                return movies_management_pb2.ActorResponse
        except Exception as e:
            self.log_trace(metadata, f"Error while getting actor: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal server error')
            return movies_management_pb2.ActorResponse

    def AddMovie(self, request, context):
        """
        Add a new movie to database
        """
        metadata = self.get_metadata(context)
        self.log_trace(metadata, f"Received request to add movie: {request.name}")

        if not self.validate_api_key(metadata, context):
            return movies_management_pb2.MovieResponse()

        try:
            id = request.id
            movie_name = request.name
            actor_names = request.actors
            director = request.director
            rating = request.rating

            movie = Movie(id, movie_name, actor_names, director, rating)

            # If movie already exists, don't add a duplicate
            if movie_name.lower() in movies_db:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Movie Already exists")
                return movies_management_pb2.AddMovieResponse()

            movies_db[movie_name.lower()] = movie

            # Get the last actor to be added and increment the id
            last_actor = list(actors_db.keys())[-1]
            last_actor_id = int(actors_db.get(last_actor).id)

            for actor in actor_names:
                if actor.lower() in actors_db:
                    actor_details = actors_db.get(actor.lower())
                    if movie not in actor_details.movie_names:
                        actor_movies = actor_details.movie_names
                        actor_movies.append(movie_name)
                        actors_db[actor] = Actor(actor_details.id, actor_details.actor_name, actor_movies)
                else:
                    last_actor_id += 1
                    actors_db[actor.lower()] = Actor(id=str(last_actor_id), actor_name=actor, movie_names=[movie_name])

            return movies_management_pb2.AddMovieResponse(
                id=movie.id,
                name=movie.name,
                actors=movie.actors,
                director=movie.director,
                rating=movie.rating,
                message="Movie created successfully"
            )
        except Exception as e:
            self.log_trace(metadata, f"Error while adding Movie: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {e}")
            return movies_management_pb2.AddMovieResponse(message='Internal server error')

    def ChangeRating(self, request, context):
        """
        Change the rating for a movie
        """
        metadata = self.get_metadata(context)
        self.log_trace(metadata, f"Received request to change rating for movie: {request.movie_name}")

        if not self.validate_api_key(metadata, context):
            return movies_management_pb2.MovieResponse()
        try:
            movie_name = request.movie_name
            rating = request.rating
            sanitized_movie_name = movie_name.lower()

            if sanitized_movie_name in movies_db:
                result_movie = movies_db.get(sanitized_movie_name)
                old_rating = result_movie.rating
                result_movie.rating = rating
                movies_db[sanitized_movie_name] = result_movie
                return movies_management_pb2.ScoreResponse(
                    id=result_movie.id,
                    movie_name=result_movie.name,
                    rating=result_movie.rating,
                    message=f"Rating changed from {old_rating} to {rating}"
                )
            else:
                # Movie not found in datbase
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Movie not found. Cannot change rating')
                return movies_management_pb2.ScoreResponse()
        except Exception as e:
            self.log_trace(metadata, f"Error while changing rating: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal server error')
            return movies_management_pb2.ScoreResponse(message='Internal server error')

    def GetMoviesByDirector(self, request, context):
        """
        Get movies by director and stream the response
        """
        metadata = self.get_metadata(context)
        self.log_trace(metadata, f"Received request for movies by director: {request.director}")

        if not self.validate_api_key(metadata, context):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid API key")
            return

        director_name = request.director
        for movie in movies_db.values():
            if movie.director == director_name:
                yield movies_management_pb2.MovieResponse(
                    id=movie.id,
                    name=movie.name,
                    actors=movie.actors,
                    director=movie.director,
                    rating=movie.rating
                )



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movies_management_pb2_grpc.add_MoviesServiceServicer_to_server(MoviesService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
