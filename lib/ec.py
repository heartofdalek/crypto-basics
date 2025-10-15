class EllipticCurve:
    def __init__(self, a, b, p):
        """
        Инициализация эллиптической кривой: y² = x³ + ax + b (mod p)
        """
        self.a = a
        self.b = b
        self.p = p
        
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
        
        # Случай, когда точки одинаковые (удвоение)
        if x1 == x2 and y1 == y2:
            return self.point_doubling(P1)
        
        # Случай, когда точки противоположные
        if x1 == x2:
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
        
        # Вычисление наклона
        s = ((3 * x**2 + self.a) * pow(2 * y, -1, self.p)) % self.p
        
        # Вычисление координат результирующей точки
        x3 = (s**2 - 2 * x) % self.p
        y3 = (s * (x - x3) - y) % self.p
        
        return (x3, y3)
    
    def scalar_multiplication(self, k, P):
        """
        Умножение точки P на скаляр k
        Используется метод double-and-add
        """
        if k == 0:
            return None
        if k == 1:
            return P
        
        result = None
        addend = P
        
        # Преобразуем k в двоичное представление
        k_bin = bin(k)[2:]
        
        for bit in k_bin:
            result = self.point_doubling(result) if result is not None else None
            
            if bit == '1':
                result = self.point_addition(result, addend)
        
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
