import pygame
import time
from heapq import heappush, heappop

# Kích thước ô trong mê cung
CELL_SIZE = 40
GRID_COLOR = (200, 200, 200)
LIGHTNING_COLOR = (255, 215, 0)
PATH_COLOR = (50, 205, 50)
START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)
WALL_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (255, 255, 255)

# Mê cung mẫu
maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]

start = (1, 1)
goal = (3, 3)

# Hàm hiển thị mê cung trên màn hình Pygame
def draw_grid(screen, maze, path=[], lightning=[], start=None, goal=None):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (i, j) == start:
                pygame.draw.rect(screen, START_COLOR, rect)
            elif (i, j) == goal:
                pygame.draw.rect(screen, GOAL_COLOR, rect)
            elif (i, j) in path:
                pygame.draw.rect(screen, PATH_COLOR, rect)
            elif (i, j) in lightning:
                pygame.draw.rect(screen, LIGHTNING_COLOR, rect)
            elif cell == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            else:
                pygame.draw.rect(screen, BACKGROUND_COLOR, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

# Hàm in mê cung ra console
def draw_console(maze, path=[], lightning=[], start=None, goal=None):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) == start:
                print("\u2b50", end=" ")
            elif (i, j) == goal:
                print("\ud83c\udfc1", end=" ")
            elif (i, j) in path:
                print("\u2022", end=" ")  # Đường đi
            elif (i, j) in lightning:
                print("\u26a1", end=" ")  # Hiệu ứng tia sét
            elif cell == 1:
                print("\u2b1b", end=" ")  # Tường
            else:
                print("\u2b1c", end=" ")  # Ô trống
        print()
    print("\n")

# Thuật toán Lightning Search
def lightning_search(screen, maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 hướng

    def manhattan(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    frontier = []
    heappush(frontier, (0, start))
    cost_so_far = {start: 0}
    came_from = {start: None}
    lightning_effect = []

    print("Mê cung ban đầu:")
    draw_console(maze, start=start, goal=goal)

    while frontier:
        _, current = heappop(frontier)

        # Hiệu ứng tia sét trên màn hình và console
        lightning_effect.append(current)
        draw_grid(screen, maze, lightning=lightning_effect, start=start, goal=goal)
        draw_console(maze, lightning=lightning_effect, start=start, goal=goal)
        pygame.display.flip()
        time.sleep(0.2)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in directions:
            next_cell = (current[0] + dx, current[1] + dy)
            if 0 <= next_cell[0] < rows and 0 <= next_cell[1] < cols and maze[next_cell[0]][next_cell[1]] == 0:
                new_cost = cost_so_far[current] + 1
                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + manhattan(next_cell[0], next_cell[1], goal[0], goal[1])
                    heappush(frontier, (priority, next_cell))
                    came_from[next_cell] = current

    return None

# Chương trình chính
def main():
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE + 70))  # Thêm vùng cho nút
    pygame.display.set_caption("Lightning Search Visualization")
    screen.fill(BACKGROUND_COLOR)

    # Vẽ mê cung ban đầu
    draw_grid(screen, maze, start=start, goal=goal)
    pygame.display.flip()

    # Tạo nút "Bắt đầu"
    font = pygame.font.Font(None, 36)
    start_button = pygame.Rect(cols * CELL_SIZE // 2 - 100, rows * CELL_SIZE + 10, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    start_text = font.render("Start", True, (255, 255, 255))
    screen.blit(start_text, (cols * CELL_SIZE // 2 - 50, rows * CELL_SIZE + 20))
    pygame.display.flip()

    running = True
    path = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if not path:
                        path = lightning_search(screen, maze, start, goal)
                        if path:
                            print("Đường đi tìm được:", path)
                            draw_console(maze, path=path, start=start, goal=goal)
                            draw_grid(screen, maze, path=path, start=start, goal=goal)
                            pygame.display.flip()
                        else:
                            print("Không tìm được đường đi!")
                            # Hiển thị thông báo trên màn hình
                            error_text = font.render("No Path Found!", True, (255, 0, 0))
                            screen.blit(error_text, (cols * CELL_SIZE // 2 - 80, rows * CELL_SIZE + 40))
                            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
