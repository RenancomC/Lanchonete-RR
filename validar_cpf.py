def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove tudo que não for número

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Valida primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10

    # Valida segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10

    return d1 == int(cpf[9]) and d2 == int(cpf[10])