def eh_bissexto(ano):
    """Verifica se um ano é bissexto."""
    return ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)

def obter_limite_dias(mes, ano):
    """Retorna a quantidade de dias que um mês possui, considerando anos bissextos."""
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif mes in [4, 6, 9, 11]:
        return 30
    elif mes == 2:
        return 29 if eh_bissexto(ano) else 28
    return 0

def calcular_dia_seguinte():
    entrada = input("Digite a data (dd/mm/aaaa): ")
    
    try:
        partes = entrada.split("/")
        
        if len(partes) != 3:
            print("Formato inválido. Por favor, utilize o formato dd/mm/aaaa.")
            return
            
        d, m, a = int(partes[0]), int(partes[1]), int(partes[2])
        
        # Validação do mês digitado
        if not (1 <= m <= 12):
            print(f"Data inválida: o mês {m} não existe.")
            return
            
        # Validação do dia digitado
        limite_dias = obter_limite_dias(m, a)
        if not (1 <= d <= limite_dias):
            print(f"Data inválida: o mês {m} do ano {a} tem apenas {limite_dias} dias.")
            return
            
        # Lógica para adicionar 1 dia
        d += 1
        
        if d > limite_dias:
            d = 1
            m += 1
            if m > 12:
                m = 1
                a += 1
                
        print(f"A data seguinte é: {d:02d}/{m:02d}/{a:04d}")

    except ValueError:
        print("Erro: Digite apenas números separados por '/'.")

if __name__ == "__main__":
    calcular_dia_seguinte()
