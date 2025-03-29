# Bài toán tìm đường đi của Pacman sử dụng thuật toán A\*

## Giới thiệu

Bài toán yêu cầu lập trình Pac-Man để thu thập tất cả các điểm thức ăn trong mê cung bằng cách sử dụng thuật toán tìm đường A\*.

## Mô hình hóa bài toán

### Biểu diễn mê cung

Mê cung được biểu diễn dưới dạng ma trận ký tự với các thành phần như sau:

- `%` : Tường (obstacle/wall)
- `P` : Vị trí ban đầu của Pac-Man
- `.` : Thức ăn (food points), có thể có nhiều điểm
- `O` : Bánh thần kỳ (magical pies), giúp Pac-Man đi xuyên tường trong 5 bước sau khi ăn
- ` ` (dấu cách): Ô trống
- Nếu Pac-Man chạm vào một góc của mê cung, nó sẽ tự động dịch chuyển đến góc đối diện.

### Biểu diễn trạng thái

Một trạng thái của Pac-Man trong mê cung bao gồm:

- **Vị trí hiện tại** của Pac-Man `(x, y)`
- **Các điểm thức ăn còn lại** trong mê cung
- **Số bước đi xuyên tường còn lại** nếu Pac-Man đã ăn bánh thần kỳ

**Ví dụ**:

Giả sử mê cung có cấu trúc như sau:

```txt
%%%%%%%%% %P . % % %%% % % %O . % %%%%%%%%%
```

Tại một thời điểm, trạng thái có thể được biểu diễn là:

```python
state = {
    "pacman_position": (1, 1),
    "food_locations": [(1, 4), (3, 4)],
    "power_steps": 0
}
```

**Giải thích:**

- Pac-Man đang ở vị trí `(1, 1)`.
- Còn 2 điểm thức ăn ở tọa độ `(1, 4)` và `(3, 4)`.
- Chưa ăn bánh thần kỳ, nên `power_steps = 0`.

Nếu Pac-Man di chuyển đến `(3, 1)` và ăn bánh thần kỳ (`O`), trạng thái mới sẽ là:

```python
state = {
    "pacman_position": (3, 1),
    "food_locations": [(1, 4), (3, 4)],
    "power_steps": 5  # Có thể đi xuyên tường trong 5 bước
}
```

Sau 3 bước di chuyển tiếp theo, `power_steps` sẽ giảm xuống còn `2`.

### Successor Function

Từ một trạng thái, Pac-Man có thể di chuyển theo 4 hướng:

- **Bắc** (North) `(x - 1, y)`
- **Nam** (South) `(x + 1, y)`
- **Đông** (East) `(x, y + 1)`
- **Tây** (West) `(x, y - 1)`

#### Quy tắc di chuyển:

- Pac-Man **không thể đi vào tường** `%` trừ khi đang chịu hiệu ứng của bánh thần kỳ.
- Nếu Pac-Man **ăn bánh thần kỳ (`O`)**, nó có thể đi xuyên tường trong **5 bước tiếp theo**.
- Pac-Man **tự động dịch chuyển** nếu đi vào một góc, xuất hiện ở góc đối diện.
- Nếu Pac-Man **di chuyển vào ô chứa thức ăn (`.`)**, thức ăn đó sẽ bị ăn mất.
- Nếu Pac-Man **đi qua ô trống (` `)**, trạng thái không thay đổi ngoài vị trí.

#### Ví dụ

Giả sử mê cung có cấu trúc như sau:

```txt
%%%%%%%%% %P . % % %%% % % %O . % %%%%%%%%%
```

**Trường hợp 1: Pac-Man chưa ăn bánh thần kỳ**
Với trạng thái:

```python
state = {
    "pacman_position": (1, 1),
    "food_locations": [(1, 4), (3, 4)],
    "power_steps": 0
}
```

Các trạng thái kế tiếp khả thi:

- Đi Đông `(1, 2)`: Hợp lệ (di chuyển vào ô trống).
- Đi Nam `(2, 1)`: Không hợp lệ (bị chặn bởi tường %).
- Đi Bắc `(0, 1)`: Không hợp lệ (bị chặn bởi tường %).
- Đi Tây `(1, 0)`: Không hợp lệ (bị chặn bởi tường %).

**Trường hợp 2: Pac-Man đã ăn bánh thần kỳ**

Nếu Pac-Man ăn bánh thần kỳ (O), trạng thái mới sẽ là:

```python
state = {
    "pacman_position": (3, 1),
    "food_locations": [(1, 4), (3, 4)],
    "power_steps": 5  # Có thể đi xuyên tường trong 5 bước
}
```

Lúc này, Pac-Man có thể đi xuyên tường:

- Đi Bắc `(2, 1)`: Hợp lệ (bình thường bị chặn, nhưng có hiệu ứng bánh thần kỳ).
- Đi Nam `(4, 1)`: Không hợp lệ (bị chặn bởi tường %, và đây không phải bước đi hợp lệ).
- Đi Đông `(3, 2)`: Hợp lệ.
- Đi Tây `(3, 0)`: Không hợp lệ.

Sau mỗi bước, `power_steps` giảm đi 1. Khi về `0`, Pac-Man không thể đi xuyên tường nữa.

### Hàm đánh giá (Heuristic)

Hàm heuristic được sử dụng là **khoảng cách Manhattan** giữa vị trí hiện tại của Pac-Man và điểm thức ăn gần nhất:

$$ h(x, y) = |x_1 - x_2| + |y_1 - y_2| $$

Trong đó:

- $(x_1, y_1)$ là vị trí hiện tại của Pac-Man
- $(x_2, y_2)$ là vị trí của điểm thức ăn gần nhất

Hàm này hoạt động tốt vì Pac-Man chỉ có thể di chuyển theo 4 hướng (lên, xuống, trái, phải), phù hợp với cách đo lường khoảng cách Manhattan.

**Ví dụ:** Giả sử Pac-Man đang ở vị trí `(2, 3)` và có thức ăn tại `(5, 6)`, heuristic được tính như sau:

$$ h(2,3) = |2 - 5| + |3 - 6| = 3 + 3 = 6 $$

### Độ chấp nhận và tính nhất quán của heuristic

#### 1️⃣ Tính chấp nhận (Admissibility)

Heuristic **chấp nhận** nếu nó không bao giờ đánh giá cao hơn chi phí thực sự để đến đích.

- Khoảng cách Manhattan **không bao giờ lớn hơn** số bước thực tế cần đi, bởi vì Pac-Man chỉ có thể di chuyển một ô mỗi bước.
- Do đó, heuristic này không đánh giá quá mức chi phí cần thiết và đảm bảo thuật toán A\* tìm ra đường đi tối ưu.

**Ví dụ:**  
Giả sử Pac-Man ở `(1, 1)` và thức ăn ở `(4, 5)`.  
Khoảng cách Manhattan là:

$$ h(1,1) = |1 - 4| + |1 - 5| = 3 + 4 = 7 $$

Nếu không có vật cản, số bước thực tế cũng là **7**, đúng bằng giá trị heuristic.  
Như vậy, heuristic này không đánh giá cao hơn chi phí thực tế.

#### 2️⃣ Tính nhất quán (Consistency)

Heuristic **nhất quán** nếu nó thỏa mãn **bất đẳng thức tam giác**:

$$ h(x, y) \leq c(x, y, x', y') + h(x', y') $$

Trong đó:

- $(x, y)$ là trạng thái hiện tại
- $(x', y')$ là trạng thái kế tiếp (một bước đi hợp lệ)
- $c(x, y, x', y')$ là chi phí của bước đi (luôn bằng **1** trong Pac-Man)

**Ví dụ:**  
Giả sử Pac-Man đang ở `(2,3)`, thức ăn ở `(5,6)`, heuristic hiện tại là:

$$ h(2,3) = |2 - 5| + |3 - 6| = 3 + 3 = 6 $$

Pac-Man di chuyển **đông** đến `(2,4)`, heuristic mới:

$$ h(2,4) = |2 - 5| + |4 - 6| = 3 + 2 = 5 $$

Ta thấy:

$$ h(2,3) - h(2,4) = 6 - 5 = 1 = c(x, y, x', y') $$

Điều này luôn đúng, nên heuristic đảm bảo tính nhất quán.

## Triển khai thuật toán A\*

### Định nghĩa thuật toán

A\* là thuật toán tìm đường sử dụng hàng đợi ưu tiên để mở rộng các trạng thái theo công thức:

\[
f(n) = g(n) + h(n)
\]

Trong đó:

- \( g(n) \) là chi phí từ trạng thái ban đầu đến trạng thái hiện tại.
- \( h(n) \) là giá trị heuristic (khoảng cách Manhattan đến điểm thức ăn gần nhất).

Thuật toán đảm bảo tìm được đường đi tối ưu nếu heuristic thỏa mãn điều kiện chấp nhận (admissibility).

### Các bước của thuật toán A\*

1️⃣ **Khởi tạo hàng đợi ưu tiên** (`frontier`) với trạng thái ban đầu:

- Định dạng: `(f(n), vị trí Pac-Man, g(n), số bước xuyên tường còn lại, đường đi đến hiện tại)`.
- Thêm trạng thái ban đầu vào hàng đợi với `g(n) = 0`.

2️⃣ **Duyệt qua các trạng thái theo thứ tự ưu tiên**:

- Lấy trạng thái có `f(n)` nhỏ nhất ra khỏi hàng đợi.
- Nếu Pac-Man đã đến vị trí thức ăn, trả về đường đi.

3️⃣ **Mở rộng trạng thái hiện tại**:

- Lấy tất cả hành động hợp lệ (`Bắc, Nam, Đông, Tây, Dừng`).
- Tạo các trạng thái con và tính toán `g(n)`, `h(n)`, `f(n)`.
- Nếu Pac-Man ăn bánh thần kỳ, cập nhật số bước xuyên tường còn lại.

4️⃣ **Cập nhật hàng đợi**:

- Nếu trạng thái con chưa được khám phá hoặc có đường đi tốt hơn, thêm vào hàng đợi.

5️⃣ **Lặp lại quá trình cho đến khi hàng đợi rỗng hoặc tìm thấy lời giải**.

### Cấu trúc hàng đợi ưu tiên

| **f(n)** | **Vị trí (x, y)** | **g(n) (cost)** | **Bước xuyên tường còn lại** | **Đường đi**                 |
| -------- | ----------------- | --------------- | ---------------------------- | ---------------------------- |
| 6        | (2,3)             | 3               | 0                            | [(1,1), (2,2), (2,3)]        |
| 8        | (4,5)             | 5               | 2                            | [(1,1), (2,2), (3,3), (4,5)] |

- **Hàng đợi sắp xếp theo `f(n)`, ưu tiên mở rộng trạng thái có `f(n)` nhỏ nhất**.
- Khi Pac-Man ăn bánh thần kỳ, **số bước xuyên tường được thiết lập lại 5** và cho phép đi qua tường.

## Pseudo code

```python
function A_STAR_SEARCH(problem, goal)
    returns a path from the initial state to the goal

    inputs:
        problem  ← an instance of the Problem class
        goal     ← target position for Pac-Man

    frontier ← priority queue containing (heuristic(problem.initial_state, goal), problem.initial_state, cost=0, power=problem.power_steps, path=[problem.initial_state])
    explored ← empty set

    while frontier is not empty do
        (priority, current_state, current_cost, current_power, current_path) ← POP(frontier)

        if current_state == goal then
            problem.power_steps ← current_power
            return current_path

        if current_state is in explored then
            continue

        add current_state to explored

        for each action in GET_ACTIONS(problem, current_state, current_power) do
            child_state ← action
            new_cost ← current_cost + 1
            new_power ← max(0, current_power - 1)

            if problem.maze[child_state] == PIE_CHAR then
                new_power ← POWER_STEP_DURATION

            if child_state is not in explored then
                PUSH(frontier, (new_cost + HEURISTIC(child_state, goal), child_state, new_cost, new_power, current_path + [child_state]))

    return null


function GET_ACTIONS(problem, state, current_power)
    returns a list of valid next states

    inputs:
        problem       ← an instance of the Problem class
        state         ← current position of Pac-Man
        current_power ← remaining power-up steps

    actions ← empty list
    (x, y) ← state
    directions ← [UP, DOWN, LEFT, RIGHT]
    corners ← GET_CORNER_POSITIONS(problem)

    if state is in corners then
        actions ← actions ∪ GET_OPPOSITE_CORNERS(problem, state)

    for each (dx, dy) in directions do
        new_x ← x + dx
        new_y ← y + dy

        if new_x, new_y is within bounds of the maze then
            cell ← problem.maze[new_x, new_y]

            if cell is not WALL_CHAR or current_power > 0 then
                add (new_x, new_y) to actions

    return actions

```

## Class Design

### `Problem`

📌 **Chức năng:** Quản lý trạng thái của trò chơi, bao gồm bản đồ, vị trí Pac-Man, vị trí thức ăn và các quy tắc di chuyển.

#### **Thuộc tính**

- **`maze`** → Bản đồ mê cung được đọc từ file.
- **`initial_state`** → Vị trí bắt đầu của Pac-Man.
- **`food_locations`** → Danh sách vị trí thức ăn trong mê cung.
- **`visited_cells`** → Lưu các ô Pac-Man đã đi qua.
- **`power_steps`** → Số bước còn lại khi Pac-Man đang có sức mạnh đặc biệt (ăn bánh Pie).

#### **Phương thức**

- **`__init__(file_path)`** → Đọc bản đồ từ file và thiết lập các giá trị ban đầu.
- **`load_maze(file_path)`** → Xác định vị trí Pac-Man và thức ăn.
- **`get_actions(state, current_power)`** → Trả về danh sách các bước đi hợp lệ của Pac-Man.
- **`get_corner_positions()`** → Xác định vị trí 4 góc của mê cung.
- **`get_opposite_corners(current_corner)`** → Xác định góc đối diện cho phép dịch chuyển.

---

### `AStar`

📌 **Chức năng:** Tìm đường đi ngắn nhất từ Pac-Man đến thức ăn bằng thuật toán **A\***.

#### **Phương thức**

- **`heuristic(a, b)`** → Tính khoảng cách Manhattan giữa hai điểm.
- **`search(problem, goal)`** → Tìm đường đi tối ưu từ vị trí Pac-Man đến mục tiêu (thức ăn), tính đến chướng ngại vật và sức mạnh đặc biệt.

---

### `MazeVisualizer`

📌 **Chức năng:** Vẽ Pac-Man, mê cung, thức ăn, tường và hiệu ứng di chuyển.

#### **Thuộc tính**

- **`problem`** → Tham chiếu đến đối tượng `Problem` để lấy thông tin mê cung.
- **`screen`** → Màn hình Pygame để vẽ trò chơi.
- **`width, height`** → Kích thước cửa sổ trò chơi dựa trên mê cung.
- **`frame_count`** → Số khung hình đã hiển thị (dùng để hiệu ứng động).
- **`pacman_mouth_open`** → Trạng thái miệng của Pac-Man (mở hoặc đóng).

#### **Phương thức**

- **`__init__(problem)`** → Khởi tạo cửa sổ hiển thị trò chơi.
- **`toggle_pacman_mouth()`** → Thay đổi trạng thái miệng của Pac-Man.
- **`draw_pacman(pacman_pos, direction)`** → Vẽ Pac-Man theo hướng di chuyển.
- **`draw(pacman_pos, direction)`** → Vẽ toàn bộ mê cung, thức ăn và Pac-Man trong mỗi bước đi.

---

### `Game`

📌 **Chức năng:** Điều khiển trò chơi, tính toán đường đi và cập nhật trạng thái trò chơi.

#### **Thuộc tính**

- **`problem`** → Lưu trạng thái mê cung và các quy tắc trò chơi.
- **`visualizer`** → Quản lý hiển thị trò chơi.

#### **Phương thức**

- **`__init__(maze_file)`** → Đọc bản đồ và khởi tạo trò chơi.
- **`run()`** → Điều khiển Pac-Man ăn hết thức ăn bằng thuật toán A\*, cập nhật màn hình trò chơi.
