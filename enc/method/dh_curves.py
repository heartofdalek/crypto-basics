from enc.method.base import Base as BaseMethod
from lib.ec import EllipticCurve

class DHCurves(BaseMethod):
    
    test_payload = [
        ( 'a', 'b', 'p', 'G', 'k1', 'k2' ),
        ( 1, 1, 23, (7, 11), 5, 16 ), # мой вариант 2, расчёт по методичке: 25 % 12 + 1
        ( 3, 5, 17, (1,3), 8, 11 ), # вариант 5
        ( 1, 1, 23, (6,4), 8, 9 ), # вариант 6
        ( 1, 0, 23, (9,5), 10, 8 ), # вариант 7
        ( 9, 17, 23, (16,5), 11, 7 ), # вариант 8
        ( 2, 3, 97, (3,6), 12, 6), # вариант 9
        ( -1, 3, 37, (2,3), 13, 5 ), # вариант 10
        ( 3, 5, 17, (1,3), 3, 13 ), # вариант 11
        ( 1, 0, 23, (9,5), 14, 4 ), # вариант 13
        ( 1, 1, 23, (3,13), 16, 2 ), # вариант 15
        ( -1, 1, 29, (9, 27), 4, 17 ), # вариант 1, где (9, 27) не лежит на кривой, можно поменять на (9,24), которая корректная и код отработает
        ( 2, 3, 97, (3,6), 6, 10 ), # вариант 3, дает None, получается точка в бесконечности
        ( -1, 3, 37, (2,3), 7, 12 ),  # вариант 4, дает None, получается точка в бесконечности
        ( 1, 1, 23, (6,4), 2, 14 ),  # вариант 12, дает None, получается точка в бесконечности
        ( 2, 3, 97, (3,6), 15, 3 ),  # вариант 14, дает None, получается точка в бесконечности
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
            raise Exception(f'Базовая точка G={G} не лежит на кривой!')
        
        # Пользователь A вычисляет свою открытую точку
        A_public = curve.scalar_multiplication(k1, G)
        
        if self.options.is_debug:
            print("Пользователь A")
            print(f"Закрытый ключ: k1 = {k1}")
            print(f"Открытый ключ: A = k1 * G = {k1} * {G} = {A_public}")
        
        # Пользователь Б вычисляет свою открытую точку
        B_public = curve.scalar_multiplication(k2, G)
        
        if self.options.is_debug:
            print("\nПользователь Б")
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
        
        # Пользователь Б вычисляет общий секрет
        shared_secret_B = curve.scalar_multiplication(k2, A_public)
        
        if self.options.is_debug:
            print("\nПользователь Б получает открытый ключ A и вычисляет:")
            print(f"K_B = k2 * A = {k2} * {A_public} = {shared_secret_B}")
            print()
        
        # Проверяем, что оба пользователя получили одинаковый секрет
        if shared_secret_A is not None and shared_secret_A == shared_secret_B:
            if self.options.is_debug:
                print(f"Оба пользователя получили одинаковый общий секрет {shared_secret_A}!")
                print(f"Общий ключ K = k1 * k2 * G = {k1} * {k2} * {G} = {shared_secret_A}")
                
                # Проверяем, что K = k1 * k2 * G
                k_product = (k1 * k2) % curve.curve_order
                K_direct = curve.scalar_multiplication(k_product, G)
                print(f"Проверка: K = ({k1} * {k2} % {curve.curve_order}) * G = {k_product} * {G} = {K_direct}\n")
        else:
            if shared_secret_A is None:
                raise Exception(f"Получен секрет {shared_secret_A}!")
            else:
                raise Exception("Пользователи получили разные секреты!")

        return f'Общий секрет: {shared_secret_A}'

    def after_load(self):
        self.key = int(self.key)
