import time
# coding: utf-8

# n to 1 policy
class N2One:
    def __init__(self, servers):
        self.servers = servers

    def select_server(self):        # Novo Pedido
        return self.servers[0]

    def update(self, *arg):         # Final Pedido
        pass


# round robin policy
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.index = -1
        self.size = len(self.servers)

    def select_server(self):
        if self.index == self.size - 1:
            self.index = 0
        else:
            self.index += 1

        usedServer = self.servers[self.index]
        return usedServer

    def update(self, *arg):
        pass


# least connections policy
class LeastConnections:
    def __init__(self, servers):
        self.servers = servers
        self.connections = dict()

        for server in servers:
            self.connections[server] = 0

    def select_server(self):
        minSize = self.connections[self.servers[0]]
        usedServer = self.servers[0]
        
        for server, numConns in self.connections.items():
            if numConns < minSize:
                minSize = numConns
                usedServer = server

        self.connections[usedServer] += 1
        return usedServer

    def update(self, *arg):
        # O *arg é uma lista de argumentos que vai o servidor a ser cancelado
        if len(arg) < 1:
            raise ValueError("ERRO: Não foi passado nenhum servidor")

        server = arg[0]
        if self.connections[server] > 0:
            self.connections[server] -= 1

# least response time
class LeastResponseTime:
    def __init__(self, servers):
        self.servers = servers
        
        self.average_response = {server: 0 for server in servers}
        
        self.initial_time_request = {server: 0 for server in servers}
        
        self.response_times = {server: [] for server in servers}


    def select_server(self):
        current_time = time.time()
        for server in self.servers:
            elapsed_time = self.initial_time_request[server] - current_time
            self.average_response[server] = (sum(self.response_times[server]) + elapsed_time) / (len(self.response_times[server]) + 1)
        
        server = min(self.average_response, key=self.average_response.get)
        self.initial_time_request[server] = time.time()
        return server

    def update(self, *arg):
        if len(arg) < 1:
            raise ValueError("No server specified for update")

        server = arg[0]
        
        response_time = time.time() - self.initial_time_request[server]
        self.response_times[server].append(response_time)

        count = len(self.response_times[server])
        self.average_response[server] = sum(self.response_times[server]) / count