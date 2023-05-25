def text_maker(fileName, debug = False):  
    from random import randint, uniform, seed

    seed()

    with open(f"{fileName}", "r") as file:
        questions = file.read().split('\n\n')

        for question in questions:
            text = question.split('\n')
            
            #print(text)
            prompt, FORMULA, input_vars = text[0], text[-1], text[1:-1]

            vars = {}
            #print(input_vars)
            for i in input_vars:
                x, min, max = i.split()
                if (float(min) % 1) == 0 and (float(max) % 1) == 0: 
                    vars[x] = (int(min), int(max))
                else:
                    vars[x] = (float(min), float(max))
            
            wrong_ans = []
            i = 0
            while i < 4:
                temp_vars = {}
                for j in vars:
                    if type(vars[j][0]) == int:
                        temp_vars[j] = randint(vars[j][0],vars[j][1])
                    else:
                        #!ROUND
                        temp_vars[j] = format(uniform(vars[j][0],vars[j][1]),'.2g')

                if i == 0:
                    correct_vars = temp_vars
                else:
                    wrong_ans.append(temp_vars)
                i += 1

            
            temp_formula = FORMULA
            for var in correct_vars.keys():
                temp_formula = temp_formula.replace(var, str(correct_vars[var]))
                
            correct_ans = eval(temp_formula)
            

            if debug:
                print(prompt)
                print(FORMULA)
                print(temp_vars)
                print()

text_maker("test_maker.txt",debug=True)

