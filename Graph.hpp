# include <bits/stdc++.h>
using namespace std;

class Coordinate {
public:
    int x, y, z;
    Coordinate() : x(0), y(0), z(0) {}
    Coordinate(int x, int y, int z) : x(x), y(y), z(z) {}

    long long get_distance_squared(Coordinate other) {
        long long dx = x - other.x;
        long long dy = y - other.y;
        long long dz = z - other.z;

        return dx * dx + dy * dy + dz * dz;
    }
};

class Node {
public:
    int id;
    Coordinate coordinate;
    Node(int id) : id(id) {}
    Node(int id, Coordinate coordinate) : id(id), coordinate(coordinate) {}

    long long get_distance_squared(Node other) {
        return coordinate.get_distance_squared(other.coordinate);
    }
};

class Edge {
public:
    Node from, to;
    long long weight_squared;
    Edge(Node from, Node to, long long weight_squared) : from(from), to(to), weight_squared(weight_squared) {}
};

class Graph {
public:
    vector<Node> nodes;
    vector<vector<long long>> adj_matrix;

    Graph(vector<Node> nodes) : nodes(nodes) {
        adj_matrix.resize(nodes.size(), vector<long long>(nodes.size(), LLONG_MAX));
        for (int i = 0; i < nodes.size(); i++) {
            for (int j = 0; j < nodes.size(); j++) {
                if (i == j) {
                    adj_matrix[i][j] = 0;
                }
                else {
                    adj_matrix[i][j] = nodes[i].get_distance_squared(nodes[j]);
                }
            }
        }
    }

    Graph(vector<Node> nodes, vector<Edge> edges) : nodes(nodes) {
        adj_matrix.resize(nodes.size(), vector<long long>(nodes.size(), LLONG_MAX));
        for (int i = 0; i < nodes.size(); i++) {
            adj_matrix[i][i] = 0;
        }
        for (Edge edge : edges) {
            adj_matrix[edge.from.id][edge.to.id] = edge.weight_squared;
            adj_matrix[edge.to.id][edge.from.id] = edge.weight_squared;
        }
    }
};