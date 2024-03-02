# include <bits/stdc++.h>
using namespace std;

class Coordinate {
public:
    int x, y, z;
    Coordinate() : x(0), y(0), z(0) {}
    Coordinate(int x, int y, int z) : x(x), y(y), z(z) {}
};

class Node {
public:
    int id;
    Coordinate coordinate;
    Node(int id) : id(id) {}
    Node(int id, Coordinate coordinate) : id(id), coordinate(coordinate) {}

    int get_distance_squared(Node other) {
        long long dx = coordinate.x - other.coordinate.x;
        long long dy = coordinate.y - other.coordinate.y;
        long long dz = coordinate.z - other.coordinate.z;

        return dx * dx + dy * dy + dz * dz;
    }
};

class Edge {
public:
    Node from, to;
    int weight_squared;
    Edge(Node from, Node to, int weight_squared) : from(from), to(to), weight_squared(weight_squared) {}
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