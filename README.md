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
