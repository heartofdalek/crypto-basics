from enc.method.base import Base as BaseMethod
from lib.ec import EllipticCurve

class DHCurves(BaseMethod):
    
    test_payload = [
        ( 'a', 'b', 'p', 'G', 'k1', 'k2' ),
        ( -1, 1, 29, (9, 27), 4, 17 ),
        ( 1, 1, 23, (7, 11), 5, 16 ), # мой вариант 2, из методички
        ( 2, 3, 97, (3,6), 6, 10 ),
        ( -1, 3, 37, (2,3), 7, 12 ),
        ( 3, 5, 17, (1,3), 8, 11 ),
        ( 1, 1, 23, (6,4), 8, 9 ),
        ( 1, 0, 23, (9,5), 10, 8 ),
        ( 9, 17, 23, (16,5), 11, 7 ), # если в консоли не указать -k, то срабатывает вариант 8 -- остаток от Лабораторной 1
        ( 2, 3, 97, (3,6), 12, 6),
        ( -1, 3, 37, (2,3), 13, 5 ),
        ( 3, 5, 17, (1,3), 3, 13 ),
        ( 1, 1, 23, (6,4), 2, 14 ),
        ( 1, 0, 23, (9,5), 14, 4 ),
        ( 2, 3, 97, (3,6), 15, 3 ),
        ( 1, 1, 23, (3,13), 16, 2 ),
    ]
    
    def action_main_task(self, payload):
        
        a, b, p, G, k1, k2 = self.test_payload[self.key]
        
        result = self.diffie_hellman_ec(a, b, p, G, k1, k2)
        
        return f'{result}'

    
    def diffie_hellman_ec(self, a, b, p, G, k1, k2):
        """
        Моделирование обмена по протоколу Диффи-Хеллмана на эллиптических кривых
        """
        if self.options.is_debug:
            print("-= ПРОТОКОЛ ДИФФИ-ХЕЛЛМАНА НА ЭЛЛИПТИЧЕСКИХ КРИВЫХ =-")
            print(f"Параметры кривой: a={a}, b={b}, p={p}")
            print(f"Базовая точка G: {G}")
            print(f"Закрытые ключи: k1={k1}, k2={k2}")
            print()
        
        # Создаем объект эллиптической кривой
        curve = EllipticCurve(a, b, p)
        
        # Проверяем корректность параметров кривой
        if not curve.is_valid():
            if self.options.is_debug:
                print(f"4a³ + 27b² = 4*{a}³ + 27*{b}² = 0 (mod {p})")
            raise Exception("Параметры кривой некорректны!")
        
        # Проверяем, что базовая точка лежит на кривой
        if not curve.is_point_on_curve(G):
            raise Exception("Базовая точка G не лежит на кривой!")
        
        # Пользователь A вычисляет свою открытую точку
        A_public = curve.scalar_multiplication(k1, G)
        
        if self.options.is_debug:
            print("Пользователь A")
            print(f"Закрытый ключ: k1 = {k1}")
            print(f"Открытый ключ: A = k1 * G = {k1} * {G} = {A_public}")
        
        # Пользователь B вычисляет свою открытую точку
        B_public = curve.scalar_multiplication(k2, G)
        
        if self.options.is_debug:
            print("\nПользователь B")
            print(f"Закрытый ключ: k2 = {k2}")
            print(f"Открытый ключ: B = k2 * G = {k2} * {G} = {B_public}")
            print()
        
        # Обмен открытыми ключами и вычисление общего секрета
        if self.options.is_debug:
            print("-> Обмен ключами <-")
        
        # Пользователь A вычисляет общий секрет
        shared_secret_A = curve.scalar_multiplication(k1, B_public)
        
        if self.options.is_debug:
            print("Пользователь A получает открытый ключ B и вычисляет:")
            print(f"K_A = k1 * B = {k1} * {B_public} = {shared_secret_A}")
        
        # Пользователь B вычисляет общий секрет
        shared_secret_B = curve.scalar_multiplication(k2, A_public)
        
        if self.options.is_debug:
            print("\nПользователь B получает открытый ключ A и вычисляет:")
            print(f"K_B = k2 * A = {k2} * {A_public} = {shared_secret_B}")
            print()
        
        # Проверяем, что оба пользователя получили одинаковый секрет
        if shared_secret_A == shared_secret_B:
            if self.options.is_debug:
                print("Оба пользователя получили одинаковый общий секрет!")
                print(f"Общий ключ K = k1 * k2 * G = {k1} * {k2} * {G} = {shared_secret_A}")
                
                # Проверяем, что K = k1 * k2 * G
                k_product = (k1 * k2) % curve.p
                K_direct = curve.scalar_multiplication(k_product, G)
                print(f"Проверка: K = ({k1} * {k2}) * G = {k_product} * {G} = {K_direct}")
        else:
            raise Exception("Пользователи получили разные секреты!")
        
        return shared_secret_A

    def after_load(self):
        self.key = int(self.key)
