'''Adding routes to your project is easy'''

class Node(object):
    '''Implements basic class for url nodes.  These nodes contain child nodes,
       variable child nodes, and/or functions.  This allows us to walk through
       the requested URL path and get the most relevant result.'''

    def __init__(self,resource=None,name=None,isvar=False):
        self.children = {}
        self.resource = resource
        self.isvar = isvar
        self.name = name
        self.varchild = None

    def add_child(self, child=None, node=None):
        self.children[child] = node

    def __repr__(self):
        return self.name

class DefaultRouter(object):
    '''This class implements the DefaultRouter.  DefaultRouter is meant to be
       used directly parse paths into callable resources, and to map requested
       urls from the client to our callable resources we mapped earlier.'''

    def __init__(self):
        self.root_node_dict = {}


    def parse_path(self, uri):
        '''Splits our path into sections using '/' as the separator.
           If the path = '/', then we map '/'.  Otherwise, we trim off the first
           item in the list as it would be blank and nondescriptive.

           The list is returned in reverse so we can pop it.'''
        if uri == '/':
            l = [uri]
        else:
            l = uri.split('/')
            if l[0] == '':
                l = l[1:]
            l.reverse()
        return l

    def add_path(self,uri,resource):
        '''takes in a path string and callable resource, calls parse_path,
           and maps that path to our callable resource.'''

        current_node = None
        root_node = None
        url = self.parse_path(uri)
        while url:
            a = url.pop()

            if root_node is None:
                if not a in self.root_node_dict:
                    root_node = Node(name=a)
                    self.root_node_dict[a] = root_node
                else:
                    root_node = self.root_node_dict[a]

                current_node = root_node

            elif current_node is not None:
                if '}' not in a:
                    if not a in current_node.children:
                        new_node = Node(name=a)
                        current_node.children[a] = new_node
                    else:
                        new_node = current_node.children[a]
                else:
                    #we found a variable.
                    if not current_node.varchild:
                        new_node = Node(name=a)
                        new_node.isvar = True
                        current_node.varchild = new_node
                    else:
                        new_node = current_node.varchild

                current_node = new_node
        current_node.resource = resource

    def return_path_resource(self,uri,var_dict):
        '''Takes in a string path, and parses it.  It uses the parsed path to
           determine what resource to call.  Raises a 404 exception if a mappped
           resource is not found.

           Also takes in var_dict.  var_dict is an existing dictionary to place
           values of parts of the url that are variables.'''


        current_node = None
        root_node = None
        url = self.parse_path(uri)

        while url:
            a = url.pop()

            if root_node is None:
                if not a in self.root_node_dict:
                    #perhaps we should allow a variable on the first node.
                    body = "404: no root node: %s" % a
                    code = '404 Not Found'
                    raise Exception(code, body)
                else:
                    root_node = self.root_node_dict[a]

                current_node = root_node

            else:

                if not a in current_node.children:
                    #we didn't find a defined path, let's try variable.
                    if not current_node.varchild:
                        #we didn't find a variable child, path is invalid.
                        code = '404 Not Found'
                        body =  "404: no child node or var found for : %s" % a
                        raise Exception(code, body)
                    else:
                        current_node = current_node.varchild
                else:
                    current_node = current_node.children[a]

            if current_node.isvar is True:
                var_dict[current_node.name] = a

        try:
            return current_node.resource
        except:
            body = "404: no root node: %s" % a
            code = '404 Not Found'
            raise Exception(code, body)