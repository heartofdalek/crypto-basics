class EllipticCurve:

    def __init__(self, a, b, p):
        """
        Инициализация эллиптической кривой: y² = x³ + ax + b (mod p)
        """
        self.a = a
        self.b = b
        self.p = p
        self.curve_order = self.find_curve_order()
        
    def is_valid(self):
        """
        Проверка корректности параметров кривой: 4a³ + 27b² ≠ 0 (mod p)
        """
        left = (4 * pow(self.a, 3, self.p)) % self.p
        right = (27 * pow(self.b, 2, self.p)) % self.p
        return (left + right) % self.p != 0
    
    def point_addition(self, P1, P2):
        """
        Сложение двух точек на эллиптической кривой
        """
        if P1 is None:
            return P2
        if P2 is None:
            return P1
            
        x1, y1 = P1
        x2, y2 = P2
        
        # Случай, когда точки одинаковые -> удвоение
        if x1 == x2 and y1 == y2:
            return self.point_doubling(P1)
        
        # Случай, когда точки противоположные
        if x1 == x2 and y1 != y2:
            #print("Складываются точка и ей противоположная, получается точка в бесконечности!")
            return None
        
        # Вычисление наклона
        s = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        
        # Вычисление координат результирующей точки
        x3 = (s**2 - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_doubling(self, P):
        """
        Удвоение точки на эллиптической кривой
        """
        if P is None:
            return None
            
        x, y = P
        
        # Если y = 0, то 2P = O
        if y == 0:
            return None
        
        # Вычисление наклона
        # print(f's = ((3 * {x}**2 + {self.a}) * pow(2 * {y}, -1, {self.p})) % {self.p}')
        s = ((3 * x**2 + self.a) * pow(2 * y, -1, self.p)) % self.p
        
        # Вычисление координат результирующей точки
        x3 = (s**2 - 2 * x) % self.p
        y3 = (s * (x - x3) - y) % self.p
        
        return (x3, y3)

    def scalar_multiplication(self, k, P):
        """
        Умножение точки на скаляр с автоматическим определением порядка
        """
        if k == 0:
            return None
        
        # Вычисляем порядок точки P
        curve_order = self.curve_order
        
        # Работаем по модулю порядка группы
        k = k % curve_order
        if k == 0:
            return None
        
        # Стандартный double-and-add
        result = None
        current = P
        
        while k > 0:
            if k & 1:
                if result is None:
                    result = current
                else:
                    result = self.point_addition(result, current)
            
            current = self.point_doubling(current)
            k >>= 1
        
        return result
    
    def is_point_on_curve(self, point):
        """
        Проверка, лежит ли точка на кривой
        """
        if point is None:
            return True
            
        x, y = point
        left = (y**2) % self.p
        right = (x**3 + self.a * x + self.b) % self.p
        return left == right
    
    def compute_order(self):
        """
        Вычисляет порядок группы и порядок базовой точки
        """
        
        # Метод 1: Полный перебор (для маленьких p)
        if self.p < 1000:  # Практический предел
            return self.find_curve_order()
        
        # Метод 2: Использование теоремы Хассе для оценки
        # Для больших p нужно использовать алгоритм Шуфа
        else:
            raise NotImplementedError("Для больших p используйте алгоритм Шуфа")
    
    def find_curve_order(self):
        """
        Находит порядок группы эллиптической кривой полным перебором
        """
        count = 1  # Учитываем точку в бесконечности
        
        for x in range(self.p):
            # Решаем y² = x³ + ax + b (mod p)
            right_side = (x**3 + self.a * x + self.b) % self.p
            # Ищем квадратные корни по модулю p
            for y in range(self.p):
                if (y * y) % self.p == right_side:
                    count += 1
                    # print(f"Точка: ({x}, {y})")
        
        return count

    def find_point_order(self, P):
        """
        Находит порядок точки P последовательным умножением
        """
        if P is None:
            return 1
        
        current = P
        order = 1
        
        while current is not None:
            order += 1
            current = self.point_addition(current, P)
            # Если вернулись к начальной точке (point_addition вернул None для противоположных)
            if current == P:
                break
        
        return order
