from textx import metamodel_from_file

query="bio:fer > 10"

metamodel = metamodel_from_file("dsl.tx")


model = metamodel.model_from_str(query)






print(model)


