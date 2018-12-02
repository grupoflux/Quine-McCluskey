import itertools

# Comparar as duas strings de binário, procurando a diferença
def compBinary(s1, s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count += 1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None

# Comparar se o número é o mesmo que o termo implicante
def compBinarySame(term, number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True

# Combinar pares e formar novo grupo
def combinePairs(group, unchecked):
    # definir tamanho
    l = len(group) - 1

    # checar lista
    check_list = []

    # criar próximo grupo
    next_group = [[] for x in range(l)]

    # varrer os grupos
    for i in range(l):
        # Primeirp grupo selecionado
        for elem1 in group[i]:
            # proximo grupo selecionado
            for elem2 in group[i+1]:
                b, pos = compBinary(elem1, elem2)
                if b == True:
                    # Juntar os grupos utilizados no check list
                    check_list.append(elem1)
                    check_list.append(elem2)
                    # trocar o bit diferente por '-'
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked

# remover listas redundantes no segundo grupo
def remove_redundant(group):
    new_group = []
    for j in group:
        new = []
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group

# remover listas redundantes no primeiro grupo
def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list

# retornar True se lista estiver vazia
def check_empty(group):

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count += 1
        if count == 0:
            return True
    return False

# Achar os primos implicantes
def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            # find essential
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True

# Achar valor máximo numa lista
def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

# multiplicar 2 termos (ex. (p1 + p2)(p1+p4+p5) ).. retorna o produto
def multiplication(list1, list2):
    list_result = []
    # se as duas listas forem vazias
    if len(list1) == 0 and len(list2) == 0:
        return list_result
    # se a lista1 for vazia
    elif len(list1) == 0:
        return list2
    # se a lista2 for vazia
    elif len(list2) == 0:
        return list1

    # se nenhuma das duas forem vazias
    else:
        for i in list1:
            for j in list2:
                # se elas tiverem termos iguais
                if i == j:
                    # list_result.append(sorted(i))
                    list_result.append(i)
                else:
                    # list_result.append(sorted(list(set(i+j))))
                    list_result.append(list(set(i+j)))
        # ordenar e remover listas redundantes
        list_result.sort()
        return list(list_result for list_result, _ in itertools.groupby(list_result))

# método de Petrick
def petrick_method(Chart):
    # P inicial
    P = []
    for col in range(len(Chart[0])):
        p = []
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)
    # multiplicar
    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l], P[l+1])

    P = sorted(P[len(P)-1], key=len)
    final = []
    # achar os termos com menor tamanho (os que têm o menor custo. Para resultados otimizados)
    min = len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break
    # final é o resultado do método Petrick
    return final

# chart = n*n lista

def find_minimum_cost(Chart, unchecked):
    P_final = []
    # essential_prime = lista com termos com somente 1 (Primos implicantes)
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)

    # Imprimir as implicações dos primos
    if len(essential_prime) > 0:
        s = "\nEssential Prime Implicants :\n"
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s = s+binary_to_letter(unchecked[i])+' , '
        #print(s[:(len(s)-3)])

    # modificar o chart para excluir os termos já utilizados
    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    # se todos forem zero, não precisa fazer o método de Petrick
    if check_all_zero(Chart) == True:
        P_final = [essential_prime]
    else:
        # método de Petrick
        P = petrick_method(Chart)

        # achar o termo de menor custo
        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count + cal_efficient(unchecked[i])
            P_cost.append(count)

        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])

        # adicionar as implicações dos primos à solução do método do Petrick
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)
    return P_final

# Calcular o número de literals
def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count += 1
    return count

# imprimir o código binário
def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        # se for uma letra entre a-z/A-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+'\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n += 1

        # condições para as próximas operações
        if c == 'z' and more == False:
            c = 'A'
        elif c == 'Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out

def main():
    n_var = int(input("Insira o número de variáves(bits): "))
    minterms = input("Insira os mintermos separados por espaços : ")
    a = minterms.split()
    # colocar os números numa lista como "int"
    a = list(map(int, a))

    group = [[] for x in range(n_var+1)]

    for i in range(len(a)):
        # converter para binário
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            # adicionar zeros para preencher o número de bits
            for j in range(n_var - len(a[i])):
                a[i] = '0' + a[i]
        # se digitar um bit incorreto
        elif len(a[i]) > n_var:
            print('\nErro : Selecione o número correto de variáveis(bits)\n')
            return
        # contar os números 1
        index = a[i].count('1')
        # agrupar os números 1 separadamente
        group[index].append(a[i])

    all_group = []
    unchecked = []
    # combinar os pares em série até que não tenha nada novo a ser combinado
    while check_empty(group) == False:
        all_group.append(group)
        next_group, unchecked = combinePairs(group, unchecked)
        group = remove_redundant(next_group)

    s = "\nImplicações dos primos :\n"
    for i in unchecked:
        s = s + binary_to_letter(i) + " , "
    print(s[:(len(s)-3)])

    # fazer o chart de implicações dos primos
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range(len(unchecked)):
            # se o termo for igual ao número comparado
            if compBinarySame(unchecked[j], a[i]):
                Chart[j][i] = 1

    # prime contém o index do termo primo imlicante
    # prime = remove_redundant_list(find_minimum_cost(Chart))
    primes = find_minimum_cost(Chart, unchecked)
    primes = remove_redundant(primes)

    print("\n--  Respostas --\n")

    for prime in primes:
        s = ''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s = s+binary_to_letter(unchecked[i])+' + '
        print(s[:(len(s)-3)])


if __name__ == "__main__":
    main()
    A = input("\nPressione enter para sair")