import random

def generate_continent(width, height, num_regions):
    """Генерирует континент с прилегающими регионами, используя клеточные автоматы."""

    # Инициализация карты случайными значениями (0 - пусто, 1-num_regions - регионы)
    grid = [[random.randint(0, num_regions) for _ in range(width)] for _ in range(height)]

    # Параметры клеточных автоматов (количество итераций, вероятность сохранения состояния)
    iterations = 10
    survival_probability = 0.5

    for _ in range(iterations):
        new_grid = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                neighbors = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            neighbors.append(grid[ny][nx])

                # Выбираем наиболее часто встречающееся значение у соседей
                if neighbors:
                    counts = {}
                    for n in neighbors:
                        counts[n] = counts.get(n, 0) + 1
                    most_common = max(counts, key=counts.get)
                    if random.random() < survival_probability:
                        new_grid[y][x] = most_common
                    else:
                        new_grid[y][x] = random.randint(1, num_regions) # Добавляем случайность для неравномерности
                else:
                    new_grid[y][x] = 0 # Край карты остаётся пустым

        grid = new_grid

    return grid


def visualize_continent(continent):
    for row in continent:
        print(''.join(str(cell) if cell !=0 else "." for cell in row))


width = 60
height = 40
num_regions = 4
continent = generate_continent(width, height, num_regions)
visualize_continent(continent)