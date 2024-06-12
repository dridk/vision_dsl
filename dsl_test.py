from textx import metamodel_from_file
# textx generate query.tx --grammar dsl.tx --target dot

def cast_value(x, operator="pass"):
    if type(x) == int :
        return f"CAST(value AS INTEGER){operator}{x}"
    if type(x) == float :
        return f"CAST(value AS FLOAT){operator}{x}"
    else :
        return f"value='{x}'"

def simple_query(element:str) -> str:
    # exemple : DOMAINE='x' value > 10
    if len(element) == 1 :
        request = f"""SELECT IPP FROM data WHERE domain='{element[0].op.field.domain}' AND key='{element[0].op.field.key}' AND {cast_value(element[0].op.val, element[0].op.op)}"""
    # exemple"bio:fer > 10 AND pmsi:cim10 = 'FT43ATC'"
    # prend le premier + l'opérateur (AND/OR):element[1] + le dernier élément 
    else : 
        if element[1] == "AND" :
            operator = "\nINTERSECT\n"
        if element[1] == "OR" :
            operator = "\nUNION\n"
        request = f"""SELECT IPP FROM data WHERE domain='{element[0].op.field.domain}' AND key='{element[0].op.field.key}' AND {cast_value(element[0].op.val, element[0].op.op)}{operator}(SELECT IPP FROM data WHERE domain='{element[-1].op.field.domain}' AND key='{element[-1].op.field.key}' AND {cast_value(element[-1].op.val, element[-1].op.op)})"""
    return request



def query_to_sql(query:str) -> str:
    metamodel = metamodel_from_file("dsl.tx")
    model = metamodel.model_from_str(query)
    # si la requête est simple (2 éléments + 1 opérateur)
    if len(model.op) <= 3 :
        return simple_query(model.op)
   
    # requêtes complexes : 
    position_dict = {}
    for i, word in enumerate(model.op):
        # Vérification mot clé
        if type(word) == str :
            value = word # garde AND/OR
        else:
            value = None
        position_dict[i] = value
        
    # 1er élément de la requête  
    request = "SELECT IPP FROM data WHERE " + f"domain='{model.op[0].op.field.domain}' AND key='{model.op[0].op.field.key}' AND {cast_value(model.op[0].op.val, model.op[0].op.op)}"
    # suppression du premier élément du dictionnaire
    del position_dict[0]
    
    for key, value in position_dict.items() :        
        if value is None: 
            request = request + f"(SELECT IPP FROM data WHERE domain='{model.op[key].op.field.domain}' AND key='{model.op[key].op.field.key}' AND {cast_value(model.op[key].op.val, model.op[0].op.op)})"
        else :
            if value == "AND" :
                operator = "\nINTERSECT\n"
            if value == "OR" :
                operator = "\nUNION\n"
            request = request + f" {operator}"
    
    return request
    



# Requêtes de test :
# ------------------------------------
# query = "bio:Fer < 10"
#query = "bio:Fer < 10.5"
# query = "pmsi:CIM10 = 'E435'"
#query = "bio:Fer > 10 OR pmsi:CIM10 = 'E30'"
# query="bio:Fer > 5 AND pmsi:CIM10 = 'E435'"
#query="bio:Fer = 10 OR pmsi:CIM10 = 'N99'"
#query="bio:Fer = 10 AND pmsi:CIM10 = 'D329' OR pmsi:CIM10 = 'C000'"
#query="bio:Fer = 10 AND pmsi:CIM10 = 'S031' OR pmsi:CIM10 = 'C000' AND pharma:CCAM = 'HBQK002'"
#query="bio:Fer = 10 AND pmsi:CIM10 = 'S031' OR pmsi:CIM10 = 'C000' AND pharma:CCAM = 'HBQK002'"
#query="bio:Fer = 10 AND pmsi:CIM10 = 'S031' OR pmsi:CIM10 = 'C000' AND pharma:CCAM = 'HBQK002' OR bio:Fer = 50"
#query="bio:Fer = 10 OR pmsi:CIM10 = 'S031' OR pmsi:CIM10 = 'C000' AND pharma:CCAM = 'HBQK002' OR bio:Fer = 50"


# result_query = query_to_sql(query)   
# print(result_query)