# Created by NaveenPiedy at 6/18/2024 6:32 AM

import grpc
import movies_management_pb2
import movies_management_pb2_grpc


def get_movies(name, metadata):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.GetMovieRequest(name=name)
            response = stub.GetMovie(request, metadata=metadata)
            print(f"Movie found \n {response} \n")

            return response
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Error: {name} is not in database. {e.details()} \n")
        else:
            print(f"Unexpected error: {e}")


def get_actors(name, metadata):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.GetActorRequest(actor_name=name)
            response = stub.GetActor(request, metadata=metadata)
            print(f"Actor found \n {response} \n")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Error: {name} is not in database. {e.details()}")
        else:
            print(f"Unexpected error: {e}")


def add_movie(id, movie_name, actors, director, rating, metadata):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.AddMovieRequest(id=id, name=movie_name, actors=actors, director=director,
                                                            rating=rating)
            response = stub.AddMovie(request, metadata=metadata)
            print(f"\n {response} \n")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            print(f"Failed to add {movie_name} because it already exists: {e}")
        else:
            print(f"Failed to add Movie: {e}")


def get_movie_by_director(director_name, metadata):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = movies_management_pb2_grpc.MoviesServiceStub(channel)

        # Test GetMoviesByDirector with streaming
        request = movies_management_pb2.GetMoviesByDirectorRequest(director=director_name)
        try:
            for response in stub.GetMoviesByDirector(request, metadata=metadata):
                print(f"Movie by Joss Whedon: {response}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


def change_rating(movie_name, rating, metadata):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = movies_management_pb2_grpc.MoviesServiceStub(channel)
            request = movies_management_pb2.ScoreRequest(movie_name=movie_name, rating=rating)
            response = stub.ChangeRating(request, metadata=metadata)
            print(f"\n {response} \n")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Error: {e.details()}")
        else:
            print(f"Unexpected error: {e}")


def run():
    metadata = [('api-key', 'secret-api-key')]
    wrong_metadata = [('api-key', 'wrong-api-key')]
    metadata_with_trace_id = [('api-key', 'secret-api-key'), ('trace-id', '12345')]
    wrong_metadata_with_trace_id = [('api-key', 'wrong-api-key'), ('trace-id', '12345')]

    get_movies('Avengers', metadata=wrong_metadata)
    """Response: 
    Unexpected error: <_InactiveRpcError of RPC that terminated with: 
    status = StatusCode.UNAUTHENTICATED
    details = "Invalid API key"
    debug_error_string = "UNKNOWN:Error received from peer ipv6:%5B::1%5D:50051
    {created_time:"2024-06-19T02:21:19.2151243+00:00", grpc_status:16, grpc_message:"Invalid API key"}"
    """

    get_movies('Avengers', metadata=wrong_metadata_with_trace_id)
    """
    Server side logging:
    WARNING:root:Invalid API key for trace ID: 12345
    """

    # Get a Particular Movie
    get_movies('Avengers', metadata=metadata)
    """Response: 
        Movie found 
        id: "1"
        name: "Avengers"
        actors: "Robert"
        actors: "Chris"
        director: "Joss Wheadon"
        rating: 4.2"""

    # Try to get a Movie not in DB
    get_movies('John Wick', metadata=metadata)
    "Response: Error: John Wick is not in database. Movie not found"

    # Get a Particular Actor
    get_actors('Robert', metadata=metadata)
    """
    Response:
    Actor found 
    id: "1"
    actor_name: "Robert"
    movie_names: "Avengers"
    """

    # Add a Movie to DB
    add_movie(id='3', movie_name="Alaipayuthey", actors=['Madhavan', 'Shalini'], director='Mani Ratnam', rating=5.0,
              metadata=metadata)
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
              rating=4.5, metadata=metadata)
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
              rating=4.5, metadata=metadata)

    """
    Response:
    Failed to add Minnale because it already exists: <_InactiveRpcError of RPC that terminated with:
    status = StatusCode.ALREADY_EXISTS
    details = "Movie Already exists"
    debug_error_string = "UNKNOWN:Error received from peer ipv6:%5B::1%5D:50051 
    {created_time:"2024-06-18T05:00:14.3717465+00:00", grpc_status:6, grpc_message:"Movie Already exists"}">
    """

    # Get an actor with two or more movies
    get_actors('madhavan', metadata=metadata)
    """
    Response:
    Actor found 
    id: "3"
    actor_name: "Madhavan"
    movie_names: "Alaipayuthey"
    movie_names: "Minnale"
    """

    # Change Rating for a movie
    change_rating("Minnale", 5.0, metadata=metadata)
    """
    Response:
    id: "4"
    movie_name: "Minnale"
    rating: 5
    message: "Rating changed from 4.5 to 5.0"
    """

    add_movie('7', 'Serenity', ["Nathan Fillion", "Gina Torres"], 'Joss Wheadon', 4.0, metadata=metadata)
    """
    Response:
     id: "7"
    name: "Serenity"
    actors: "Nathan Fillion"
    actors: "Gina Torres"
    director: "Joss Wheadon"
    rating: 4
    message: "Movie created successfully"
    """

    get_movie_by_director('Joss Wheadon', metadata=metadata)
    """
    Movie by Joss Whedon: id: "1"
    name: "Avengers"
    actors: "Robert"
    actors: "Chris"
    director: "Joss Wheadon"
    rating: 4.2

    Movie by Joss Whedon: id: "7"
    name: "Serenity"
    actors: "Nathan Fillion"
    actors: "Gina Torres"
    director: "Joss Wheadon"
    rating: 4
    """


if __name__ == '__main__':
    run()
