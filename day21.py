
def read_input(file_name):
    foods = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            end_of_ingredients = line.index(" (")
            ingredients = set(line[0:end_of_ingredients].split(" "))
            allergens = set(line[end_of_ingredients+11:-1].split(", "))
            foods.append((ingredients, allergens))
    return foods

def part1(foods):
    all_ingredients = set()
    all_allergens = set()
    for food in foods:
        all_ingredients = all_ingredients.union(food[0])
        all_allergens = all_allergens.union(food[1])
    # print("all ingredients and allergens")
    # print(all_ingredients)
    # print(all_allergens)

    allergen_to_ingredient = { allergen:all_ingredients.copy() for allergen in all_allergens }
    # ingredient_to_allergen = { ingredient:all_allergens.copy() for ingredient in all_ingredients }
    for food in foods:
        for allergen in food[1]:
            allergen_to_ingredient[allergen] = allergen_to_ingredient[allergen].intersection(food[0])
    print(allergen_to_ingredient)

    ingredients_with_no_possible_allergens = all_ingredients.copy()
    for possible_allergenic_ingredient in allergen_to_ingredient.values():
        ingredients_with_no_possible_allergens = ingredients_with_no_possible_allergens.difference(possible_allergenic_ingredient)

    # Example: kfcds, nhms, sbzzf, or trh can't be in any allergens
    print(ingredients_with_no_possible_allergens)

    count_safe_occurrences = 0
    for food in foods:
        safe_ingredients = ingredients_with_no_possible_allergens.intersection(food[0])
        count_safe_occurrences += len(safe_ingredients)
    return (count_safe_occurrences, allergen_to_ingredient)


def part2(foods, allergen_to_ingredient):
    while True:
        changes = False
        for (allergen, possible_ingredients) in allergen_to_ingredient.items():
            if len(possible_ingredients) == 1:
                for the_ingredient in possible_ingredients:
                    for (other_allergen, other_ingredients) in allergen_to_ingredient.items():
                        if other_allergen != allergen and the_ingredient in other_ingredients:
                            other_ingredients.remove(the_ingredient)
                            changes = True
                        
        if not changes:
            break
    # print(allergen_to_ingredient)

    # Now sort by allergen, form canonical key
    canonical_key = ""
    for a in sorted(allergen_to_ingredient.keys()):
        canonical_key += allergen_to_ingredient[a].pop() + ","
    return canonical_key[0:-1]

foods = read_input('day21_input.txt')
# foods = read_input('day21_example_input.txt')
# for l in foods: print(l)

(count_safe_occurrences, allergen_to_ingredient) = part1(foods)
print(f"Part 1: {count_safe_occurrences}")
# My answer to part 1: 2734
part2_answer = part2(foods, allergen_to_ingredient)
print("Part 2: {}".format(part2_answer))
# My answer to part 2: kbmlt,mrccxm,lpzgzmk,ppj,stj,jvgnc,gxnr,plrlg
