resources = [
    [101, "Laptop", "Electronics", 8],
    [102, "Projector", "Electronics", 0],
    [103, "Whiteboard", "Classroom", 5],
    [104, "Microphone", "Audio", 3],
    [105, "Camera", "Electronics", 2]
]


def print_resource(resource):
    res_id, name, category, quantity = resource
    line = f"ID: {res_id} | {name} | {category} | Quantity: {quantity}"
    if quantity < 0:
        line += "  <-- INVALID (negative quantity)"
    print(line)


def display_resources(resources):
    if len(resources) == 0:
        print("No resources to display.")
        return
    for resource in resources:
        print_resource(resource)


def search_by_category(resources, category):
    found = False
    for resource in resources:
        if resource[2].lower() == category.lower():
            print_resource(resource)
            found = True
    if not found:
        print(f"No resources found in category '{category}'.")


def find_unavailable(resources):
    unavailable = []
    for resource in resources:
        if resource[3] == 0:
            unavailable.append(resource)
    if len(unavailable) == 0:
        print("All resources are available.")
    else:
        for resource in unavailable:
            print_resource(resource)
    return unavailable


def find_resource_by_id(resources, res_id):
    for resource in resources:
        if resource[0] == res_id:
            return resource
    return None


def show_resource_by_id(resources, res_id):
    resource = find_resource_by_id(resources, res_id)
    if resource is None:
        print(f"Resource ID {res_id} not found.")
    else:
        print_resource(resource)


print("=== All resources ===")
display_resources(resources)

print("\n=== Category: Electronics ===")
search_by_category(resources, "Electronics")

print("\n=== Unavailable resources ===")
find_unavailable(resources)

print("\n=== Test 1: unknown resource ID ===")
show_resource_by_id(resources, 999)

print("\n=== Test 2: negative quantity ===")
bad_data = [[106, "Speaker", "Audio", -4]]
display_resources(bad_data)
find_unavailable(bad_data)

print("\n=== Test 3: resource with zero units ===")
find_unavailable(resources)

print("\n=== Test 4: empty resource list ===")
display_resources([])
search_by_category([], "Audio")
find_unavailable([])
