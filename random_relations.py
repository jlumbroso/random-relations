import itertools
import random


def universe_of_relation(relation):
    flat_list = [element for pair in relation for element in pair]
    return sorted(set(flat_list))


def generate_random_universe(size=None, superset=None):
    if size is None:
        size = random.randint(1, 10)

    if superset is None:
        superset = list(range(1, size * 10))

    universe = random.sample(superset, size)

    # Attempt sorting, if elements are comparable
    try:
        return sorted(universe)
    except:
        pass

    return universe


## GENERATION METHODS


def generate_random_relation_by_erdos(universe, p=0.5):
    return [(x, y) for x in universe for y in universe if random.random() < p]


def generate_random_reflexive_relation_by_erdos(universe, p=0.5):
    relation = [(x, x) for x in universe]  # Ensure reflexivity
    relation += [
        (x, y) for x in universe for y in universe if x != y and random.random() < p
    ]
    return relation


def generate_random_symmetric_relation_by_erdos(universe, p=0.5):
    temp_relation = [
        (x, y) for x in universe for y in universe if x <= y and random.random() < p
    ]
    symmetric_relation = temp_relation + [(y, x) for x, y in temp_relation if x != y]
    return symmetric_relation


def generate_uniform_random_relation(universe):
    all_possible_pairs = list(itertools.product(universe, repeat=2))
    num_pairs = random.randint(0, len(all_possible_pairs))
    selected_pairs = random.sample(all_possible_pairs, num_pairs)
    return selected_pairs


def generate_uniform_random_relation_with_rejection(
    universe,
    min_target_size=None,
    max_target_size=None,
    rejection_methods=None,
    max_rejections=None,
):
    all_possible_pairs = list(itertools.product(universe, repeat=2))

    rejection_count = 0

    while True:
        print(rejection_count)
        if max_rejections is not None and rejection_count >= max_rejections:
            raise ValueError("max rejections reached")

        num_pairs = random.randint(0, len(all_possible_pairs))

        # Reject by size

        if min_target_size is not None and num_pairs < min_target_size:
            rejection_count += 1
            continue

        if max_target_size is not None and num_pairs > max_target_size:
            rejection_count += 1
            continue

        # Draw the actual sample

        selected_pairs = random.sample(all_possible_pairs, num_pairs)

        # Reject by property testing

        if rejection_methods is None:
            break
        else:
            reject = False
            for rejection_method in rejection_methods:
                if not rejection_method(selected_pairs):
                    reject = True
                    break

            if reject:
                rejection_count += 1
                continue

    return selected_pairs


## CHECKING METHODS


def is_reflexive(relation, universe):
    relation_set = set(relation)  # Convert list of tuples to set for faster lookup
    return all((x, x) in relation_set for x in universe)


def is_symmetric(relation, universe):
    relation_set = set(relation)
    return all((b, a) in relation_set for a, b in relation)


def is_transitive(relation, universe):
    relation_set = set(relation)
    return all(
        (a, c) in relation_set
        for a, b in relation_set
        for c in universe
        if (b, c) in relation_set
    )


def is_assymetric(relation, universe):
    relation_set = set(relation)
    return all((b, a) not in relation_set for a, b in relation_set if a != b)


def is_antisymmetric(relation, universe):
    relation_set = set(relation)
    return all((b, a) not in relation_set for a, b in relation_set if a != b)


def is_irreflexive(relation, universe):
    relation_set = set(relation)
    return all((x, x) not in relation_set for x in universe)


def is_equivalence_relation(relation, universe):
    return (
        is_reflexive(relation, universe)
        and is_symmetric(relation, universe)
        and is_transitive(relation, universe)
    )


def is_order_relation(relation, universe):
    return (
        is_reflexive(relation, universe)
        and is_antisymmetric(relation, universe)
        and is_transitive(relation, universe)
    )


def is_total_order(relation, universe):
    return is_order_relation(relation, universe) and all(
        (x, y) in relation for x in universe for y in universe if x != y
    )


def is_partial_order(relation, universe):
    return is_order_relation(relation, universe)


## FINDING MISSING PAIRS


def find_missing_pairs_to_reflexive(relation, universe):
    relation_set = set(relation)
    missing = [(x, x) for x in universe if (x, x) not in relation_set]
    return missing


def find_missing_pairs_to_symmetric(relation, universe):
    relation_set = set(relation)
    missing = [(b, a) for a, b in relation if (b, a) not in relation_set]
    return missing


def find_missing_pairs_to_transitive(relation, universe):
    relation_set = set(relation)
    missing = []
    for a, b in relation_set:
        for c in universe:
            if (b, c) in relation_set and (a, c) not in relation_set:
                missing.append((a, c))
    return list(set(missing))  # Remove duplicates


def find_missing_pairs_to_assymetric(relation, universe):
    relation_set = set(relation)
    conflicting = [(b, a) for a, b in relation_set if (b, a) in relation_set and a != b]
    return conflicting


def find_missing_pairs_to_antisymmetric(relation, universe):
    relation_set = set(relation)
    conflicting = [(b, a) for a, b in relation_set if (b, a) in relation_set and a != b]
    return conflicting


## FINDING CONFLICTING PAIRS


def find_conflict_pairs_for_antisymmetry(relation):
    relation_set = set(relation)
    conflicts = [(a, b) for a, b in relation_set if (b, a) in relation_set and a != b]
    return conflicts


def find_conflict_pairs_for_asymmetry(relation):
    relation_set = set(relation)
    conflicts = [(a, b) for a, b in relation_set if (b, a) in relation_set]
    return conflicts


def find_conflict_pairs_for_irreflexivity(relation):
    conflicts = [(a, a) for a, a in relation if a == a]
    return conflicts


## PRETTY PRINTING


def pretty_print_relation_properties(
    relation, universe, include_missing_pairs=False, include_conflicting_pairs=False
):
    # Check various properties
    reflexive = is_reflexive(relation, universe)
    symmetric = is_symmetric(relation, universe)
    transitive = is_transitive(relation, universe)
    asymmetric = is_assymetric(relation, universe)
    antisymmetric = is_antisymmetric(relation, universe)
    irreflexive = is_irreflexive(relation, universe)
    equivalence = is_equivalence_relation(relation, universe)
    order = is_order_relation(relation, universe)

    # Create a formatted string to print each property and its status
    print("Relation Properties:")
    print(f"  Universe: {universe}")
    print(f"  Relation: {relation}")
    print("  Properties:")
    print(f"    Reflexive: {'Yes' if reflexive else 'No'}")
    print(f"    Symmetric: {'Yes' if symmetric else 'No'}")
    print(f"    Transitive: {'Yes' if transitive else 'No'}")
    print(f"    Asymmetric: {'Yes' if asymmetric else 'No'}")
    print(f"    Antisymmetric: {'Yes' if antisymmetric else 'No'}")
    print(f"    Irreflexive: {'Yes' if irreflexive else 'No'}")
    print(f"    Equivalence Relation: {'Yes' if equivalence else 'No'}")
    print(f"    Partial/Total Order Relation: {'Yes' if order else 'No'}")

    # Missing and conflicting pairs
    if include_missing_pairs:
        print()
        if not reflexive:
            missing_reflexive = find_missing_pairs_to_reflexive(relation, universe)
            print(f"    Missing pairs to be reflexive: {missing_reflexive}")
        if not symmetric:
            missing_symmetric = find_missing_pairs_to_symmetric(relation, universe)
            print(f"    Missing pairs to be symmetric: {missing_symmetric}")
        if not transitive:
            missing_transitive = find_missing_pairs_to_transitive(relation, universe)
            print(f"    Missing pairs to be transitive: {missing_transitive}")

    if include_conflicting_pairs:
        print()
        if asymmetric:
            conflicting_asymmetric = find_conflict_pairs_for_asymmetry(relation)
            print(f"    Conflicting pairs for asymmetry: {conflicting_asymmetric}")
        if antisymmetric:
            conflicting_antisymmetric = find_conflict_pairs_for_antisymmetry(relation)
            print(
                f"    Conflicting pairs for antisymmetry: {conflicting_antisymmetric}"
            )
        if irreflexive:
            conflicting_irreflexive = find_conflict_pairs_for_irreflexivity(relation)
            print(f"    Conflicting pairs for irreflexivity: {conflicting_irreflexive}")


## Combined methods


def pin_method_list_universe(method_list, universe):
    # Create a new list to store the new methods
    new_method_list = []

    # Process each method in the input list
    for method in method_list:
        # Define a new method that wraps the original method with the universe argument
        def new_method(relation):
            return method(relation, universe)

        # Add the new method to the new list
        new_method_list.append(new_method)

    return new_method_list


def name_list_to_method_list(property_string):
    # Split the input string by commas and strip whitespace
    properties = property_string.split(",")
    method_list = []

    # Define a dictionary to map property names to their corresponding methods
    property_to_method = {
        "reflexive": random_relations.is_reflexive,
        "symmetric": random_relations.is_symmetric,
        "transitive": random_relations.is_transitive,
        "asymmetric": random_relations.is_assymetric,
        "antisymmetric": random_relations.is_antisymmetric,
        "irreflexive": random_relations.is_irreflexive,
        "equivalence": random_relations.is_equivalence_relation,
        "order": random_relations.is_order_relation,
    }

    # Process each property name
    for prop in properties:
        # Remove whitespace and convert to lowercase
        prop = prop.strip().lower()
        negate = prop.startswith("!")

        # If negated, strip the '!' from the property name
        if negate:
            prop = prop[1:]

        # Fetch the method corresponding to the property, or use a placeholder if not found
        method = property_to_method.get(prop, lambda relation, universe: None)

        # If the property needs to be negated, wrap the original method
        if negate:
            method_list.append(
                lambda relation, universe, method=method: not method(relation, universe)
            )
        else:
            method_list.append(method)

    return method_list


import random_relations


def generate_relation_with_properties(
    universe=None,
    universe_size=None,
    universe_superset=None,
    target_size=None,
    min_target_size=None,
    max_target_size=None,
    epsilon=0.0,
    property_string="",
    sort_result=True,
):

    # Determine the universe if it is not provided
    if not universe:
        if universe_size:
            if universe_superset:
                universe = random.sample(
                    universe_superset, min(universe_size, len(universe_superset))
                )
            else:
                universe = list(
                    range(universe_size)
                )  # Generate a simple numeric universe
        else:
            if not universe_superset:
                raise ValueError("Universe size or superset must be provided")
            universe = universe_superset

    # Adjust target size based on min/max or epsilon
    if target_size:
        min_target_size = int(target_size * (1 - epsilon))
        max_target_size = int(target_size * (1 + epsilon))
    # elif not min_target_size and not max_target_size:
    #     raise ValueError("Target size or min/max target size must be specified")

    # Parse the properties to form the rejection methods
    method_list = name_list_to_method_list(property_string)
    # pin_method_list_universe = lambda methods: [
    #     lambda relation: method(relation, universe) for method in methods
    # ]
    rejection_methods = pin_method_list_universe(method_list, universe=universe)

    # Generate the relation
    relation = random_relations.generate_uniform_random_relation_with_rejection(
        universe,
        rejection_methods=rejection_methods,
        min_target_size=min_target_size,
        max_target_size=max_target_size,
    )

    # Optionally sort the relation
    if sort_result:
        relation = sorted(relation)

    return relation
