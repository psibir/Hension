import re
import argparse

class HensionRelationships:
    def __init__(self, file_path):
        self.file_path = file_path
        self.relationships = self._read_relationships_file()

    def _read_relationships_file(self):
        relationships = {}
        with open(self.file_path, 'r') as file:
            for line in file:
                match = re.match(r'\[(\d+)\] \[Department: ([^\]]+)\] \[Owner: ([^\]]+)\]', line)
                if match:
                    node_id, department, owner = match.groups()
                    relationships[int(node_id)] = {'department': department, 'owner': owner}
        return relationships

    def filter_nodes(self, target_department=None, target_owner=None):
        filtered_nodes = []
        for node_id, attributes in self.relationships.items():
            if (not target_department or attributes['department'] == target_department) and \
               (not target_owner or attributes['owner'] == target_owner):
                filtered_nodes.append(node_id)
        return filtered_nodes

def main():
    parser = argparse.ArgumentParser(description='Filter Hension nodes based on department and/or owner.')
    parser.add_argument('--department', help='Filter nodes by department')
    parser.add_argument('--owner', help='Filter nodes by owner')
    args = parser.parse_args()

    relationships = HensionRelationships('node_relationships.txt')

    filtered_nodes = relationships.filter_nodes(target_department=args.department, target_owner=args.owner)

    print("Filtered Nodes:", filtered_nodes)

if __name__ == '__main__':
    main()
