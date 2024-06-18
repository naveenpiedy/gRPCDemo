# Created by NaveenPiedy at 6/18/2024 6:32 AM

import grpc
import movies_management_pb2
import movies_management_pb2_grpc


def get_movies(name):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.GetMovieRequest(name=name)
            response = stub.GetMovie(request)
            print(f"Movie found \n {response} \n")

            return response
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Error: {name} is not in database. {e.details()} \n")
        else:
            print(f"Unexpected error: {e}")


def get_actors(name):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.GetActorRequest(actor_name=name)
            response = stub.GetActor(request)
            print(f"Actor found \n {response} \n")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Error: {name} is not in database. {e.details()}")
        else:
            print(f"Unexpected error: {e}")


def add_movie(id, movie_name, actors, director, rating):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.AddMovieRequest(id=id, name=movie_name, actors=actors, director=director,
                                                            rating=rating)
            response = stub.AddMovie(request)
            print(f"\n {response} \n")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            print(f"Failed to add {movie_name} because it already exists: {e}")
        else:
            print(f"Failed to add Movie: {e}")


def change_rating(movie_name, rating):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.ScoreRequest(movie_name=movie_name, rating=rating)
            response = stub.ChangeRating(request)
            print(f"\n {response} \n")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Error: {e.details()}")
        else:
            print(f"Unexpected error: {e}")


def run():
    # Get a Particular Movie
    get_movies('Avengers')
    """Response: 
        Movie found 
        id: "1"
        name: "Avengers"
        actors: "Robert"
        actors: "Chris"
        director: "Joss Wheadon"
        rating: 4.2"""

    # Try to get a Movie not in DB
    get_movies('John Wick')
    "Response: Error: John Wick is not in database. Movie not found"

    # Get a Particular Actor
    get_actors('Robert')
    """
    Response:
    Actor found 
    id: "1"
    actor_name: "Robert"
    movie_names: "Avengers"
    """

    # Add a Movie to DB
    add_movie(id='3', movie_name="Alaipayuthey", actors=['Madhavan', 'Shalini'], director='Mani Ratnam', rating=5.0)
    """
    Response:
     id: "3"
    name: "Alaipayuthey"
    actors: "Madhavan"
    actors: "Shalini"
    director: "Mani Ratnam"
    rating: 5
    message: "Movie created successfully"
    """

    add_movie(id='4', movie_name="Minnale", actors=['Madhavan', 'Reema Sen'], director='Gautham Vasudev Menon',
              rating=4.5)
    """ 
    Response:
    id: "4"
    name: "Minnale"
    actors: "Madhavan"
    actors: "Reema Sen"
    director: "Gautham Vasudev Menon"
    rating: 4.5
    message: "Movie created successfully"
    """

    # Check what happens when you add a duplicate Movie
    add_movie(id='4', movie_name="Minnale", actors=['Madhavan', 'Reema Sen'], director='Gautham Vasudev Menon',
              rating=4.5)

    """
    Response:
    Failed to add Minnale because it already exists: <_InactiveRpcError of RPC that terminated with:
    status = StatusCode.ALREADY_EXISTS
    details = "Movie Already exists"
    debug_error_string = "UNKNOWN:Error received from peer ipv6:%5B::1%5D:50051 
    {created_time:"2024-06-18T05:00:14.3717465+00:00", grpc_status:6, grpc_message:"Movie Already exists"}">
    """

    # Get an actor with two or more movies
    get_actors('madhavan')
    """
    Response:
    Actor found 
    id: "3"
    actor_name: "Madhavan"
    movie_names: "Alaipayuthey"
    movie_names: "Minnale"
    """

    # Change Rating for a movie
    change_rating("Minnale", 5.0)
    """
    Response:
    id: "4"
    movie_name: "Minnale"
    rating: 5
    message: "Rating changed from 4.5 to 5.0"
    """


if __name__ == '__main__':
    run()
