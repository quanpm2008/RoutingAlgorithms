####################################################
# DVrouter.py
# Name:
# HUID:
#####################################################

import json
from router import Router
from packet import Packet  # Import lớp Packet

class DVrouter(Router):
    """Distance vector routing protocol implementation.

    Add your own class fields and initialization code (e.g. to create forwarding table
    data structures). See the `Router` base class for docstrings of the methods to
    override.
    """

    def __init__(self, addr, heartbeat_time):
        Router.__init__(self, addr)  # Initialize base class - DO NOT REMOVE
        self.heartbeat_time = heartbeat_time
        self.last_time = 0
        self.distance_vector = {addr: 0}  # Khoảng cách đến chính nó là 0
        self.forwarding_table = {}  # Bảng chuyển tiếp
        self.neighbors = {}  # Lưu thông tin về các lân cận (port, endpoint, cost)

    def handle_packet(self, port, packet):
        if packet.is_traceroute:
            # Gửi gói tin dựa trên bảng chuyển tiếp
            if packet.dst_addr in self.forwarding_table:
                next_port = self.forwarding_table[packet.dst_addr]
                self.send(next_port, packet)
        elif packet.is_routing:
            # Chuyển đổi nội dung từ chuỗi JSON thành dictionary
            neighbor_vector = json.loads(packet.content)
            updated = False
            for dest, cost in neighbor_vector.items():
                new_cost = self.neighbors[port]["cost"] + cost
                if dest not in self.distance_vector or new_cost < self.distance_vector[dest]:
                    self.distance_vector[dest] = new_cost
                    self.forwarding_table[dest] = port
                    updated = True
            # Nếu có thay đổi, phát sóng vector khoảng cách mới
            if updated:
                self.broadcast_distance_vector()

    def handle_new_link(self, port, endpoint, cost):
        self.neighbors[port] = {"endpoint": endpoint, "cost": cost}
        if endpoint not in self.distance_vector or cost < self.distance_vector[endpoint]:
            self.distance_vector[endpoint] = cost
            self.forwarding_table[endpoint] = port
            self.broadcast_distance_vector()

    def handle_remove_link(self, port):
        if port in self.neighbors:
            del self.neighbors[port]
        # Xóa các đích liên quan đến cổng này
        to_remove = [dest for dest, p in self.forwarding_table.items() if p == port]
        for dest in to_remove:
            del self.distance_vector[dest]
            del self.forwarding_table[dest]
        self.broadcast_distance_vector()

    def handle_time(self, time_ms):
        if time_ms - self.last_time >= self.heartbeat_time:
            self.last_time = time_ms
            self.broadcast_distance_vector()

    def broadcast_distance_vector(self):
        for port in self.neighbors:
            # Chuyển đổi distance_vector thành chuỗi JSON
            content = json.dumps(self.distance_vector)
            packet = Packet(Packet.ROUTING, self.addr, None, content=content)
            self.send(port, packet)

    def __repr__(self):
        return f"DVrouter(addr={self.addr}, dv={self.distance_vector})"
