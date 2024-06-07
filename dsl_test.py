from textx import metamodel_from_file
import duckdb
# textx generate query.tx --grammar dsl.tx --target dot

query="bio:fer > 10 AND pmsi:cim10 = 'FT43ATC' OR pmsi:cim10 = 'TRAFGRT'"
query="bio:fer > 10 AND pmsi:cim10 = 'FT43ATC'"
#query="bio:fer > 10 AND pmsi:cim10 = 'FT43ATC' OR pmsi:cim10 = 'TRAFGRT' AND pharma:ccam > 100"

# metamodel = metamodel_from_file("dsl.tx")
# model = metamodel.model_from_str(query)
# print(model.op[0].op.field.key)

def simple_query(query:str) -> str:
    # prend un requête simple 
    for i, word in enumerate(query):
        print(i, word)


def query_to_sql(query:str) -> str:
    metamodel = metamodel_from_file("dsl.tx")
    model = metamodel.model_from_str(query)
    # print(model.op[0].op.field.key)

    if len(model.op) <= 3 :
        return simple_query(model.op)

    position_dict = {}
    
    for i, word in enumerate(model.op):
        # Vérification mot clé
        if type(word) == str :
            value = "pass"
        else:
            value = None
        position_dict[i] = value

    if type(model.op[0].op.val) == int:
        request = "SELECT IPP FROM data WHERE " + f"domain='{model.op[0].op.field.domain}' AND key='{model.op[0].op.field.key}' AND value{model.op[0].op.op}{model.op[0].op.val}"
    else : 
        request = "SELECT IPP FROM data WHERE " + f"domain='{model.op[0].op.field.domain}' AND key='{model.op[0].op.field.key}' AND value{model.op[0].op.op}'{model.op[0].op.val}'"
        
    # suppression du premier élément du dictionnaire
    del position_dict[0]

    # INTERSECT
    request = request + " INTERSECT ("
   
    for key, value in position_dict.items() :
        # Si None = pas un mots-clés
        if value is None:
            if type(model.op[key].op.val) == int:
                request = request + f" SELECT IPP FROM data WHERE domain='{model.op[key].op.field.domain}' AND key='{model.op[key].op.field.key}' AND value{model.op[key].op.op}{model.op[key].op.val} UNION"
            else : 
                request = request + f" SELECT IPP FROM data WHERE domain='{model.op[key].op.field.domain}' AND key='{model.op[key].op.field.key}' AND value{model.op[key].op.op}'{model.op[key].op.val}' UNION"
    
        # elif value != None:
            # request = request + f" {value} "
    request = request + ")"
    request = request.replace("UNION)", ")")
    print(request)
    
   # print(model.op[0].op.val)

'''
SELECT  IPP FROM table 
WHERE domain = bio AND key = Fer AND valeur > 10

INTERSECT(
    SELECT  IPP FROM table 
    WHERE domain = pmsi AND key = cim10 AND valeur = I32
UNION
    SELECT  IPP FROM table 
    WHERE domain = pmsi AND key = ccam AND valeur = 452
)
'''



query_to_sql(query)   






# programmme python > prompt = requete : affiche résultat  
# requête + compliqué 