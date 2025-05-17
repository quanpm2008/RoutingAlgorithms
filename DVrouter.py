import json
from router import Router
from packet import Packet


class DVrouter(Router):
    """Distance Vector routing protocol implementation with full recomputation on topology changes."""

    INFINITY = float('inf')

    def __init__(self, addr, heartbeat_time):
        """Initialize the DVrouter with address and heartbeat time."""
        super().__init__(addr)
        self.heartbeat_time = heartbeat_time
        self.last_time = 0
        # Routing table: dest -> (cost, port)
        self.routing_table = {addr: (0, None)}
        # Neighbor info: neighbor_addr -> (cost, port)
        self.neighbors = {}
        # Store last received distance vector from each neighbor
        self.neighbor_vectors = {}

    def handle_packet(self, port, packet):
        """Process incoming packet."""
        if packet.is_traceroute:
            # Forward traceroute based on routing table
            if packet.dst_addr in self.routing_table:
                next_port = self.routing_table[packet.dst_addr][1]
                if next_port is not None:
                    self.send(next_port, packet)
        else:
            # Distance vector update
            try:
                neighbor_addr = packet.src_addr
                vector = json.loads(packet.content)
                # Store the latest vector
                self.neighbor_vectors[neighbor_addr] = vector
                updated = self._recompute_routes()
                if updated:
                    self.broadcast_distance_vector()
            except json.JSONDecodeError:
                pass

    def handle_new_link(self, port, endpoint, cost):
        """Handle new link addition."""
        # Add to neighbor info
        self.neighbors[endpoint] = (cost, port)
        # Initialize neighbor vector to infinity for all known dests
        self.neighbor_vectors.setdefault(endpoint, {})
        updated = self._recompute_routes()
        if updated:
            self.broadcast_distance_vector()

    def handle_remove_link(self, port):
        """Handle link removal."""
        # Identify neighbor
        remove_addr = None
        for addr, (_c, p) in self.neighbors.items():
            if p == port:
                remove_addr = addr
                break
        if remove_addr:
            # Remove neighbor and its vector
            del self.neighbors[remove_addr]
            self.neighbor_vectors.pop(remove_addr, None)
        # Recompute entire table
        updated = self._recompute_routes()
        if updated:
            self.broadcast_distance_vector()

    def handle_time(self, time_ms):
        """Periodic broadcast."""
        if time_ms - self.last_time >= self.heartbeat_time:
            self.last_time = time_ms
            self.broadcast_distance_vector()

    def _recompute_routes(self):
        """Recompute routing table using distance vector algorithm."""
        new_table = {self.addr: (0, None)}
        # Add direct neighbors
        for nbr, (cost, port) in self.neighbors.items():
            new_table[nbr] = (cost, port)
        # Iterative relaxation
        updated = False
        changed = True
        while changed:
            changed = False
            for nbr, vector in self.neighbor_vectors.items():
                if nbr not in self.neighbors:
                    continue
                nbr_cost, nbr_port = self.neighbors[nbr]
                for dest, dcost in vector.items():
                    if dest == self.addr:
                        continue
                    total = nbr_cost + dcost
                    if dest not in new_table or total < new_table[dest][0]:
                        new_table[dest] = (total, nbr_port)
                        changed = True
        # Check if table changed
        if new_table != self.routing_table:
            self.routing_table = new_table
            return True
        return False

    def broadcast_distance_vector(self):
        """Broadcast distance vector to all neighbors."""
        vector = {dest: cost for dest, (cost, _) in self.routing_table.items()}
        packet = Packet(
            kind=Packet.ROUTING,
            src_addr=self.addr,
            dst_addr=None,
            content=json.dumps(vector)
        )
        for port in list(self.links.keys()):
            self.send(port, packet)

    def __repr__(self):
        return f"DVrouter(addr={self.addr}, table={self.routing_table}, neighbors={self.neighbors})"
