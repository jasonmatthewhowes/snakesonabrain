import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import *
from urllib.parse import urlparse

class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id, query_params ) = parsed

            if resource == "owners":
                if id is not None:
                    response = get_single_owner(id)
                else:
                    response = get_all_owners(query_params)
            elif resource == "snakes":
                if id is not None:
                    response = get_single_snake(id)
                    if response["species_id"]==2:
                        self._set_headers(405)
                        response = {}
                else:
                    response = get_all_snakes(query_params)
            elif resource == "species":
                if id is not None:
                    response = get_single_species(id)
                else:
                    response = get_all_species(query_params)
            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()

        else: # There is a ? in the path, run the query param functions
            (resource, query, query_params ) = parsed

            # see if the query dictionary has an email key
            if query_params[0] == "_sortBy=location" and resource == 'animals':
                 response = get_all_animals(query_params)
            elif query_params[0] == "_sortBy=customer" and resource == 'animals':
                 response = get_all_animals(query_params)
            elif query.get('email') and resource == 'customers':
                response = get_customers_by_email(query['email'][0])
            elif query.get('location_id') and resource == 'animals':
                response = get_animals_by_location(query['location_id'][0])
            elif query.get('location_id') and resource == 'employees':
                response = get_employees_by_location(query['location_id'][0])
            elif query.get('status') and resource == 'animals':
                response = get_animals_by_status(query['status'][0])
            elif query.get('status') and resource == 'animals':
                response = get_animals_by_status(query['status'][0])

   
            
        self.wfile.write(json.dumps(response).encode())
    
    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params ) = self.parse_url(self.path)

        # Initialize new animal
        new_item = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_item = create_animal(post_body)
        elif resource == "locations":
            new_item = create_location(post_body)
        elif resource == "employees":
            new_item = create_employee(post_body)
        elif resource == "customers":
            new_item = create_customer(post_body)

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_item).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id, query_params ) = self.parse_url(self.path)

        success = False

 
        if resource == "animals":
          success = update_animal(id, post_body)
        elif resource == "locations":
          success = update_location(id, post_body)
        elif resource == "customers":
          success = update_customer(id, post_body)
        elif resource == "employees":
          success = update_employee(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)  

    # Encode the new animal and send in response
        self.wfile.write("".encode())

            
    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id, query_params ) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        elif resource == "locations":
            delete_location(id)
        elif resource == "customers":
            delete_customer(id)
        elif resource == "employees":
            delete_employee(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())
            
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    
    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
