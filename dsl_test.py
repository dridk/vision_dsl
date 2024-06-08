from textx import metamodel_from_file
# textx generate query.tx --grammar dsl.tx --target dot


def simple_query(element:str) -> str:
    # prend un requête simple : "bio:fer > 10 AND pmsi:cim10 = 'FT43ATC'"
    # prend le premier et le dernier élément 
    if element[1] == "AND":
        request = f"""
        SELECT IPP FROM data WHERE domain='{element[0].op.field.domain}' AND key='{element[0].op.field.key}' AND value{element[0].op.op}{element[0].op.val}
        AND IPP IN (SELECT IPP FROM data WHERE domain='{element[-1].op.field.domain}' AND key='{element[-1].op.field.key}' AND value{element[-1].op.op}{element[-1].op.val})
        """
    if element[1] == "OR":
        request = f"""
        SELECT IPP FROM data WHERE domain='{element[0].op.field.domain}' AND key='{element[0].op.field.key}' AND value{element[0].op.op}{element[0].op.val}
        OR (domain='{element[-1].op.field.domain}' AND key='{element[-1].op.field.key}' AND value{element[-1].op.op}{element[-1].op.val})
        """
    return request


def query_to_sql(query:str) -> str:
    metamodel = metamodel_from_file("dsl.tx")
    model = metamodel.model_from_str(query)
    # si la requête est simple (2 éléments)
    if len(model.op) <= 3 :
        return simple_query(model.op)
    # requêtes complexes : 
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
    # chaque élément est inséré précédé d'UNION
    for key, value in position_dict.items() :
        # Si None = pas un mots-clés
        if value is None:
            if type(model.op[key].op.val) == int:
                request = request + f"SELECT IPP FROM data WHERE domain='{model.op[key].op.field.domain}' AND key='{model.op[key].op.field.key}' AND value{model.op[key].op.op}{model.op[key].op.val} UNION "
            else : 
                request = request + f"SELECT IPP FROM data WHERE domain='{model.op[key].op.field.domain}' AND key='{model.op[key].op.field.key}' AND value{model.op[key].op.op}'{model.op[key].op.val}' UNION "

    request = request + ")"
    request = request.replace(" UNION )", ")")

    return request
    



# Requêtes de test :
# ------------------------------------
query="bio:Fer = 10 AND pmsi:CIM10 = 'D329' OR pmsi:CIM10 = 'C000'"
# query="bio:Fer = 10 AND pmsi:CIM10 = 'E435'"
# query="bio:Fer = 10 OR pmsi:CIM10 = 'N99'"
# query="bio:Fer = 10 AND pmsi:CIM10 = 'S031' OR pmsi:CIM10 = 'C000' AND pharma:CCAM = 'HBQK002'"
# query="bio:Fer = 10 AND pmsi:CIM10 = 'S031' OR pmsi:CIM10 = 'C000' AND pharma:CCAM = 'HBQK002' OR bio:Fer = 50"


result_query = query_to_sql(query)   
print(result_query)